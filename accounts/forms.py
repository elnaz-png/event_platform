from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserRegistrationForm(forms.ModelForm):
    
    password = forms.CharField(widget=forms.PasswordInput, label='رمز عبور')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='تکرار رمز عبور')
    email = forms.EmailField(required=True, label='ایمیل')
    
   
    user_type = forms.ChoiceField(choices=Profile.UserType.choices, label='نقش شما')
    phone_number = forms.CharField(max_length=15, required=False, label='شماره تلفن')

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        labels = {
            'username': 'نام کاربری',
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("رمز عبور و تکرار آن مطابقت ندارند.")