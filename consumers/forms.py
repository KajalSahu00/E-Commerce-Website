from django import forms
from .models import Customer, CustomerProfile

class CustomerForm(forms.ModelForm):
    mobile = forms.CharField(min_length=10, max_length=10, widget=forms.TextInput(attrs={"placeholder": "Mobile Number*"}))
    class Meta:
        model = Customer
        fields = ('mobile', )

class CustomerSignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password*"}))
    name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Full Name*"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email*"}))
    class Meta:
        model = CustomerProfile
        fields = ('password', 'name', 'email', 'gender')

class CustomerLoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password*"}))
    class Meta:
        model = CustomerProfile
        fields = ('password', )