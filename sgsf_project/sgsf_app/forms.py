from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Order

class SignupForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer_name', 'phone_number', 'address']
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Full name'}),
            'phone_number': forms.TextInput(attrs={'class': 'forms-input', 'placeholder': "Phone number"}),
            'address': forms.Textarea(attrs={'class': 'form-textarea', 'placeholder': 'Delivery address'}),
        }