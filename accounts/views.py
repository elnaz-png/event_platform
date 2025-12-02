from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegistrationForm
from .models import Profile


def signup_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password']) 
            user.save()

           
            Profile.objects.create(
                user=user,
                user_type=form.cleaned_data['user_type'],
                phone_number=form.cleaned_data['phone_number']
            )

           
            login(request, user)
            return redirect('events:list') 
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            return redirect('events:list')
    else:
        form = AuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('events:list')