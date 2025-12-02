from django import forms
from .models import Ticket

class TicketForm(forms.ModelForm):
    
    coupon_code = forms.CharField(
        max_length=50, 
        required=False, 
        label='کد تخفیف',
        help_text='اگر کد تخفیف دارید، اینجا وارد کنید.'
    )

    class Meta:
        model = Ticket
        fields = ['quantity'] 
        labels = {
            'quantity': 'تعداد نفرات',
        }
        widgets = {
            'quantity': forms.NumberInput(attrs={'min': 1, 'max': 10}),
        }

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity < 1:
            raise forms.ValidationError("حداقل باید یک بلیط انتخاب کنید.")
        return quantity