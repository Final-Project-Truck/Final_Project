from django.db import models


class BaseCompany(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=200, null=True)
    confirm_password = models.CharField(max_length=200, null=True)
    phone_number = models.CharField(max_length=255)
    address = models.CharField(max_length=100, null=True, blank=True, default="")
    legal_papers = models.FileField()
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}'


class JobPosting(models.Model):
    job_title = models.CharField(max_length=100)
    company = models.ForeignKey(BaseCompany, on_delete=models.CASCADE, related_name='jobs')
    description = models.TextField(max_length=300)
    salary = models.CharField(max_length=20)


class Company(BaseCompany):
    company_name = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=100)
    description = models.TextField(max_length=250)

    def __str__(self):
        return f'{self.name}'