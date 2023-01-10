from django.contrib import admin
from baseuser.models import BaseUsers
from company.models import Company

# Register your models here.
admin.site.register(Company)
admin.site.register(BaseUsers)
