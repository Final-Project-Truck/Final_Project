from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from company.models import Company, JobPosting
from company.serializers import CompanySerializer, JobPostingSerializer


class CompanyAPIViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class JobPostingAPIViewSet(ModelViewSet):
    queryset = JobPosting.objects.all()
    serializer_class = JobPostingSerializer
