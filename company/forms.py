from django import forms
from .models import Company


class CompanyRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = Company
        fields = ['name', 'email', 'password', 'confirm_password', 'phone_number', 'address', 'legal_papers']
