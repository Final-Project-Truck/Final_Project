from rest_framework.serializers import ModelSerializer

from .models import Company, JobPosting, JobPostComment


class CompanySerializer(ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class JobPostingSerializer(ModelSerializer):
    class Meta:
        model = JobPosting
        exclude = ['company']


class JobPostCommentSerializer(ModelSerializer):
    class Meta:
        model = JobPostComment
        exclude = ['author']
