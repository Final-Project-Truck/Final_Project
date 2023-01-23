from django.contrib.auth.models import User
from django.db import models
from company.models import Company

type_choices = [
    ('per', 'Person'),
    ('com', 'Company')
]

company_type = [
    ('pub', 'Public'),
    ('pri', 'Private'),
    ('sel', 'Self-Employed'),
    ('oth', 'Other'),
]


class BaseUsers(models.Model):
    username = models.CharField(max_length=200, null=True)
    password1 = models.CharField(max_length=200, null=True)
    password2 = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True, unique=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    django_user = models.OneToOneField(User, on_delete=models.CASCADE,
                                       related_name='baseuser')
    user_type = models.CharField(max_length=3, choices=type_choices)

    def __str__(self):
        return f'{self.username}'


class UserProfile(models.Model):
    base_user = models.OneToOneField(BaseUsers, on_delete=models.CASCADE,

                                     related_name='profile')
    current_company = models.ForeignKey(Company, null=True, blank=True,
                                        on_delete=models.CASCADE,
                                        related_name='current_company')
    past_companies = models.ManyToManyField(Company, blank=True,
                                            related_name='past_companies')
    picture = models.ImageField(upload_to='profile_images',
                                default='profile_images/default.jpg')
    about = models.TextField(max_length=250, null=True)


class CompanyProfile(models.Model):
    base_user = models.OneToOneField(BaseUsers, on_delete=models.CASCADE,
                                     related_name='company_profile')
    company = models.OneToOneField(Company, on_delete=models.RESTRICT,
                                   related_name='company_user')
    website = models.URLField()
    number_of_employees = models.IntegerField()
    organization_type = models.CharField(max_length=3, choices=company_type)
    revenue = models.IntegerField()

    def __str__(self):
        return f'{self.company}'
