from django import forms
from django.contrib.auth.models import User

from baseuser.models import BaseUsers


# class BaseUsersForm(forms.ModelForm):
#     class Meta:
#         model = BaseUsers
#         fields = ['username', 'email', 'password1', 'password2', 'user_type']
#         widgets = {
#             'password1': forms.PasswordInput(),
#             'password2': forms.PasswordInput(),
#         }
#
#     def clean_password2(self):
#         password1 = self.cleaned_data.get('password1')
#         password2 = self.cleaned_data.get('password2')
#         if password1 and password2 and password1 != password2:
#             raise forms.ValidationError("Passwords don't match")
#         return password2
#
#     def save(self):
#         djangouser = User.objects.create_user(
#             username=self.cleaned_data['username'],
#             email=self.cleaned_data['email'],
#             password=self.cleaned_data['password1'])
#         BaseUsers.objects.create(
#             django_user=djangouser,
#             user_type=self.cleaned_data['user_type'])
