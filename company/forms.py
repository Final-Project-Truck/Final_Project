from django import forms
from .models import Company

class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'location', 'description']


class CompanyRegistrationForm(UserRegistrationForm):
    class Meta:
        model = Company
        fields = UserRegistrationForm.Meta.fields + ['name', 'location', 'description']