from django.contrib.auth.models import User
from django.db import models


class Company(models.Model):
    username = models.CharField(max_length=255, null=True, unique=True)
    website = models.URLField(max_length=255, null=True, unique=True)
    email = models.EmailField(max_length=255, null=True, unique=True)
    password = models.CharField(max_length=255, null=True)
    confirm_password = models.CharField(max_length=255, null=True)
    django_user = models.OneToOneField(User, on_delete=models.CASCADE,
                                       related_name='company')

    def __str__(self):
        return f'{self.username}'


class Exist_Company(models.Model):
    name = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=100)
    description = models.TextField(max_length=250)

    def __str__(self):
        return f'{self.name}'


class JobPosting(models.Model):
    job_title = models.CharField(max_length=100)
    company = models.ForeignKey(Company,
                                on_delete=models.CASCADE, related_name='jobs')
    description = models.TextField(max_length=300)
    salary = models.CharField(max_length=20)
