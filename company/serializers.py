from rest_framework.serializers import ModelSerializer

from .models import Company, JobPosting, JobPostComment


class CompanySerializer(ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class JobPostCommentSerializer(ModelSerializer):
    class Meta:
        model = JobPostComment
        exclude = ['author']


class JobPostingSerializer(ModelSerializer):
    comments = JobPostCommentSerializer(many=True, read_only=True)

    class Meta:
        model = JobPosting
        exclude = ['company']
