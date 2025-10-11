from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomerUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        mudel = User
        fields = ['username', 'email', 'password1', 'password2']
