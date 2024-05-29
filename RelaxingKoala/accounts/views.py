from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm
from django.contrib.auth.decorators import login_required
from .models import Customer, Staff


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')  
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            print(f"Authenticating user: {username} with password: {password}")  # Debugging statement
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('menu:order_menu')  # Redirect to the menu after login
            else:
                print("Authentication failed")  # Debugging statement
        else:
            print("Form is not valid")  # Debugging statement
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def home(request):
    if request.user.is_authenticated:
        # User is logged in, redirect to menu page
        return redirect('menu:order_menu')
    else:
        # User is not logged in, render login page
        return render(request, 'accounts:login')

