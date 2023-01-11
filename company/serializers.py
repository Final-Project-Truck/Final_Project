from rest_framework.serializers import ModelSerializer

from .models import Company, JobPosting


class CompanySerializer(ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class JobPostingSerializer(ModelSerializer):
    class Meta:
        model = JobPosting
        fields = '__all__'
