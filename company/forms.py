from django.forms import ModelForm
from company.models import Company


class CompanyRegistrationForm(ModelForm):

    class Meta:
        model = Company
        fields = ['username', 'website', 'email', 'password',
                  'confirm_password']