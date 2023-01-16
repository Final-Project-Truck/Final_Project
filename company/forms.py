from django import forms
from django.forms import ModelForm
from company.models import Company


class CompanyRegistrationForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Company
        fields = ['username', 'website', 'email', 'password',
                  'confirm_password']