from django.db import models


# Create your models here.
class RequestCounter(models.Model):
    route = models.CharField(max_length=100)
    counter = models.IntegerField(default=0)
