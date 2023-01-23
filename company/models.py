from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=100)
    description = models.TextField(max_length=250)

    def __str__(self):
        return f'{self.name}'


class JobPosting(models.Model):
    job_title = models.CharField(max_length=100)
    company = models.ForeignKey("baseuser.CompanyProfile",
                                on_delete=models.CASCADE,
                                related_name='jobs_company')
    description = models.TextField(max_length=300)
    salary = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.job_title}'


class JobPostComment(models.Model):
    post = models.ForeignKey(JobPosting, on_delete=models.CASCADE,
                             related_name='comments')
    author = models.ForeignKey("baseuser.BaseUsers", on_delete=models.CASCADE)
    text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True, null=True)
