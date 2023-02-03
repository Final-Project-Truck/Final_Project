from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Company, JobPosting, JobPostComment, PostLike


class CompanySerializer(ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class JobPostCommentSerializer(ModelSerializer):
    class Meta:
        model = JobPostComment
        exclude = ['author']


class JobPostingSerializer(ModelSerializer):
    is_liked = serializers.BooleanField(read_only=True)
    # likes = serializers.IntegerField()
    comments = JobPostCommentSerializer(many=True, read_only=True)

    class Meta:
        model = JobPosting
        exclude = ['company']


class PostLikeSerializer(ModelSerializer):
    """
    Serializer for PostLike model.
    """
    user = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()

    class Meta:
        model = PostLike
        fields = '__all__'

    def get_user(self, obj):
        """
        Returns the username of the user who liked the post
        """
        return obj.user.username

    def get_like_count(self, obj):
        """
        Returns the number of likes on a post
        """
        return obj.post.likes.count()

    def create(self, validated_data):
        """
        Overrides the create method to set the user to the current user
        """
        validated_data['user'] = self.context['request'].user.baseuser
        return super().create(validated_data)
