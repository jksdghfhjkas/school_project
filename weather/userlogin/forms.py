from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'class': "form-input"}))
    password1 = forms.CharField(label="Password1", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Password2', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
