from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class BaseUsers(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    django_user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='baseuser')