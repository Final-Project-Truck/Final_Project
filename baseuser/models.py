from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class BaseUsers(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    django_user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='baseuser')


class Profile(models.Model):
    base_user = models.OneToOneField(BaseUsers, on_delete=models.CASCADE, related_name='profile')
    current_company = models.ForeignKey('Company', null=True, blank=True, on_delete=models.CASCADE)
    past_companies = models.ManyToManyField('Company', null=True, blank=True)
    picture = models.ImageField(upload_to='profile_images', default='tinyurl.com/2a382vsm')
    about = models.TextField(max_length=250, null=True)


