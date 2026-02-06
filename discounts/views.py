from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from events.models import Event
from .models import DiscountCode
from .forms import DiscountForm
import logging 

logger = logging.getLogger(__name__) 

@login_required
def discount_create(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    
    if event.organizer != request.user:
        logger.warning(f"Security Alert: User {request.user.username} tried to CREATE discount for event {event_id} without permission.")
        return HttpResponseForbidden("شما اجازه تعریف تخفیف برای این رویداد را ندارید.")

    if request.method == 'POST':
        form = DiscountForm(request.POST)
        if form.is_valid():
            discount = form.save(commit=False)
            discount.event = event  
            discount.save()
            logger.info(f"Discount created: Code '{discount.code}' (%{discount.percent}) for Event {event.id} by {request.user.username}")
            messages.success(request, f"کد تخفیف '{discount.code}' با موفقیت ساخته شد.")
            return redirect('events:dashboard', pk=event.pk) 
    else:
        form = DiscountForm()
    
    return render(request, 'discounts/discount_form.html', {'form': form, 'event': event})

@login_required
def discount_delete(request, pk):
    discount = get_object_or_404(DiscountCode, pk=pk)
    event = discount.event
    
    if event.organizer != request.user:
        logger.warning(f"Security Alert: User {request.user.username} tried to DELETE discount {pk} without permission.")
        return HttpResponseForbidden("شما اجازه حذف این کد را ندارید.")

    if request.method == 'POST':
        code_name = discount.code
        discount.delete()
        logger.info(f"Discount deleted: Code '{code_name}' for Event {event.id} removed by {request.user.username}")
        messages.success(request, "کد تخفیف حذف شد.")
        return redirect('events:dashboard', pk=event.pk)
        
    return render(request, 'discounts/discount_confirm_delete.html', {'discount': discount})