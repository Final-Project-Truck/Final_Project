from django import forms
from .models import BaseCompany


class CompanyRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = BaseCompany
        fields = ['name', 'email', 'password', 'confirm_password',
                  'phone_number', 'address', 'legal_papers']
