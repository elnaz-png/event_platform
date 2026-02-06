from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout ,authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from .forms import UserRegistrationForm
from .models import Profile
import logging


logger = logging.getLogger(__name__)

def signup_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            
            # ساخت آبجکت کاربر (هنوز ذخیره نهایی نشده)
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            
            
            user.is_active = False 
            
            user.save()

            # ساخت پروفایل
            Profile.objects.create(
                user=user,
                user_type=form.cleaned_data['user_type'],
                phone_number=form.cleaned_data['phone_number']
            )

            #پروسه ارسال ایمیل فعال‌سازی
            current_site = get_current_site(request)
            mail_subject = 'فعال‌سازی حساب کاربری'
            
            # ساخت متن ایمیل از روی فایل HTML
            message = render_to_string('accounts/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)), # کد کردن آیدی کاربر
                'token': default_token_generator.make_token(user),  # ساخت توکن امنیتی
            })
            
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()

            #  ثبت لاگ 
            logger.info(f"Activation email sent to new user: {user.username} | Role: {form.cleaned_data['user_type']}")

            
            return HttpResponse('ثبت‌نام اولیه انجام شد. لطفاً برای فعال‌سازی حساب، لینک ارسال شده به ایمیل خود را کلیک کنید.')
            
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            
            logger.info(f"User logged in successfully: {user.username}")
            
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            return redirect('events:list')
        else:
            
            username_tried = request.POST.get('username', 'Unknown')
            logger.warning(f"Failed login attempt for username: '{username_tried}'")
            
    else:
        form = AuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        username = request.user.username 
        logout(request)
        
        
        logger.info(f"User logged out: {username}")
        
        return redirect('events:list')
    
    
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        logger.info(f"User activated account via email: {user.username}")
        return redirect('events:list')
    else:
        return HttpResponse('لینک فعال‌سازی نامعتبر یا منقضی شده است.')
