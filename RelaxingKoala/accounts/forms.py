from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import User, Customer, Staff  

class LoginForm(forms.Form):
    username = forms.CharField(max_length=254, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'name', 'contact', 'is_customer', 'is_staff_member']
   