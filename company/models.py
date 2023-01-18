from django.db import models


class Company(models.Model):
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


class CompanySearch(models.Model):
    com_search = models.ForeignKey(Company, on_delete=models.CASCADE,
                                   related_name='companysearch')
    pub_date = models.DateTimeField('date published', null=True)
    author = models.CharField(max_length=200)

    def __str__(self):
        return self.com_search.name