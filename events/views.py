from django.shortcuts import render, get_object_or_404 , redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.db.models import Sum , Q
from django.contrib import messages
import logging
from .models import Event
from .forms import EventForm
from tickets.models import Ticket


logger = logging.getLogger(__name__)


def event_list(request):
    
    events = Event.published_objects.published()
    
    search_query = request.GET.get('q')
    
    if search_query:
        events = events.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    events = events.order_by('-event_time')
    
    context = {
        'events': events,
        'search_query': search_query
    }
    return render(request, 'events/event_list.html', context)

def event_detail(request, pk):
   
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'events/event_detail.html', {'event': event})

@login_required
def event_create(request):
    
    if request.user.profile.user_type != 'ORGANIZER':
        return HttpResponseForbidden("شما اجازه دسترسی به این صفحه را ندارید.")

    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            
            event = form.save(commit=False)
            event.organizer = request.user 
            event.save()
            logger.info(f"New event created: '{event.title}' by organizer {request.user.username}")
            return redirect('events:list')
    else:
        form = EventForm()
    
    return render(request, 'events/event_form.html', {'form': form})


@login_required
def event_dashboard(request, pk):

    event = get_object_or_404(Event, pk=pk)
    
    if event.organizer != request.user:
        logger.warning(f"Security Alert: User {request.user.username} tried to access DASHBOARD of event {pk} without permission.")
        return HttpResponseForbidden("شما دسترسی به داشبورد این رویداد را ندارید.")
    
    
    tickets = Ticket.objects.filter(event=event).select_related('buyer')
    
   
    total_sold = tickets.aggregate(Sum('quantity'))['quantity__sum'] or 0
    total_revenue = tickets.aggregate(Sum('final_price'))['final_price__sum'] or 0
    
    context = {
        'event': event,
        'tickets': tickets,
        'total_sold': total_sold,
        'total_revenue': total_revenue,
    }
    return render(request, 'events/event_dashboard.html', context)


@login_required
def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)
    
    
    if event.organizer != request.user:
        logger.warning(f"Security Alert: User {request.user.username} tried to edit event {pk} but is not the owner.")
        return HttpResponseForbidden("شما اجازه ویرایش این رویداد را ندارید.")

    if request.method == 'POST':
    
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            logger.info(f"Event updated: '{event.title}' (id: {event.pk}) was modified by {request.user.username}")
            messages.success(request, "رویداد با موفقیت ویرایش شد.")
            return redirect('events:dashboard', pk=event.pk)
    else:
        
        form = EventForm(instance=event)
    
    return render(request, 'events/event_form.html', {'form': form, 'title': 'ویرایش رویداد'})

@login_required
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    

    if event.organizer != request.user:
        logger.warning(f"Security Alert: User {request.user.username} tried to DELETE event {pk} without permission.")
        return HttpResponseForbidden("شما اجازه حذف این رویداد را ندارید.")

    if request.method == 'POST':
        
        event.delete()
        logger.info(f"Event deleted: '{event.title}' (ID: {pk}) by {request.user.username}")
        messages.success(request, "رویداد با موفقیت حذف شد.")
        return redirect('events:list')
        
    return render(request, 'events/event_confirm_delete.html', {'event': event})

@login_required
def my_events(request):

    if request.user.profile.user_type != 'ORGANIZER':
        return HttpResponseForbidden("شما برگزارکننده نیستید.")
        
    events = Event.objects.filter(organizer=request.user).order_by('-created_at')
    
    return render(request, 'events/my_events.html', {'events': events})