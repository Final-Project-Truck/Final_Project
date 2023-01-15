from django.contrib.auth.models import User
from django.db import models
from company.models import Company


class BaseUser(models.Model):
    username = models.CharField(max_length=200, null=True)
    password1 = models.CharField(max_length=200, null=True)
    password2 = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True, unique=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    django_user = models.OneToOneField(User, on_delete=models.CASCADE,
                                       related_name='baseuser')

    def __str__(self):
        return f'{self.username}'


class Profile(models.Model):
    base_user = models.OneToOneField(BaseUser, on_delete=models.CASCADE,
                                     related_name='profile')
    current_company = models.ForeignKey(Company, null=True, blank=True,
                                        on_delete=models.CASCADE,
                                        related_name='current_company')
    past_companies = models.ManyToManyField(Company, blank=True,
                                            related_name='past_companies')
    picture = models.ImageField(upload_to='profile_images',
                                default='tinyurl.com/2a382vsm')
    about = models.TextField(max_length=250, null=True)
