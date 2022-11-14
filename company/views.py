from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from company.models import Company
from company.serializers import CompanySerializer


class CompanyAPIViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
