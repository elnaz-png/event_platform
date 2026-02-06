from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from events.models import Event
from .models import Ticket
from .forms import TicketForm
from discounts.models import DiscountCode
from payments.models import Transaction
import logging

logger = logging.getLogger(__name__)

@login_required
def ticket_purchase(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    
    if event.capacity:
        current_sales = event.tickets.count()
        if current_sales >= event.capacity:
            messages.error(request, "متاسفانه ظرفیت این رویداد تکمیل شده است.")
            return redirect('events:detail', pk=event_id)

    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            coupon_code_str = form.cleaned_data['coupon_code']
            
    
            base_price = event.price * quantity
            final_price = base_price
            discount_obj = None

            
            if coupon_code_str:
                try:
                    
                    discount_obj = DiscountCode.objects.get(
                        code=coupon_code_str, 
                        event=event, 
                        is_active=True
                    )
                   
                    discount_amount = (base_price * discount_obj.percent) / 100
                    final_price = base_price - discount_amount
                    
                except DiscountCode.DoesNotExist:
                    messages.error(request, "کد تخفیف نامعتبر است.")
                    
                    return render(request, 'tickets/purchase.html', {'form': form, 'event': event})

            
            ticket = Ticket.objects.create(
                event=event,
                buyer=request.user,
                quantity=quantity,
                applied_discount=discount_obj,
                final_price=final_price
            )

            
            Transaction.objects.create(
                buyer=request.user,
                ticket=ticket,
                amount=final_price,
                status=Transaction.TransactionStatus.SUCCESS, 
                tracking_code=f"TRX-{timezone.now().timestamp()}" 
            )
            
            logger.info(f"Ticket purchased: User {request.user.username} bought {quantity} tickets for event {event.title}. code: {ticket.ticket_code}")

            messages.success(request, f"خرید با موفقیت انجام شد! کد بلیط شما: {ticket.ticket_code}")
            return redirect('events:list') 
            
    else:
        form = TicketForm()

    return render(request, 'tickets/purchase.html', {'form': form, 'event': event})

@login_required
def ticket_list(request):
    tickets = Ticket.objects.filter(buyer=request.user).select_related('event').order_by('-registered_at')
    context = {
        'tickets': tickets
        
    }
    
    return render(request, 'tickets/ticket_list.html', context)

