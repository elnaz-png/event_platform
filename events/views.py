from django.shortcuts import render, get_object_or_404
from .models import Event
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .forms import EventForm
from django.db.models import Sum
from tickets.models import Ticket
from django.db.models import Q


def event_list(request):

    events = Event.objects.filter(status=Event.EventStatus.PUBLISHED)
    search_query = request.GET.get('q')
    
    if search_query:
        events = events.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    events = events.order_by('-event_time')
    return render(request, 'events/event_list.html', {'events': events, 'search_query':search_query})


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
            return redirect('events:list')
    else:
        form = EventForm()
    
    return render(request, 'events/event_form.html', {'form': form})


@login_required
def event_dashboard(request, pk):

    event = get_object_or_404(Event, pk=pk)
    
    if event.organizer != request.user:
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
        return HttpResponseForbidden("شما اجازه ویرایش این رویداد را ندارید.")

    if request.method == 'POST':
    
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "رویداد با موفقیت ویرایش شد.")
            return redirect('events:dashboard', pk=event.pk)
    else:
        
        form = EventForm(instance=event)
    
    return render(request, 'events/event_form.html', {'form': form, 'title': 'ویرایش رویداد'})

@login_required
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    

    if event.organizer != request.user:
        return HttpResponseForbidden("شما اجازه حذف این رویداد را ندارید.")

    if request.method == 'POST':
        
        event.delete()
        messages.success(request, "رویداد با موفقیت حذف شد.")
        return redirect('events:list')
        
    return render(request, 'events/event_confirm_delete.html', {'event': event})

@login_required
def my_events(request):

    if request.user.profile.user_type != 'ORGANIZER':
        return HttpResponseForbidden("شما برگزارکننده نیستید.")
        
    events = Event.objects.filter(organizer=request.user).order_by('-created_at')
    
    return render(request, 'events/my_events.html', {'events': events})