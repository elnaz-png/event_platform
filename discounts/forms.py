from django import forms
from .models import DiscountCode

class DiscountForm(forms.ModelForm):
    class Meta:
        model = DiscountCode
        fields = ['code', 'percent', 'usage_limit', 'is_active']
        labels = {
            'code': 'عنوان کد تخفیف',
            'percent': 'درصد تخفیف',
        }

    def clean_percent(self):
        percent = self.cleaned_data.get('percent')
        if not (0 < percent <= 100):
            raise forms.ValidationError("درصد تخفیف باید بین ۱ تا ۱۰۰ باشد.")
        return percent