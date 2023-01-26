from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, \
    HyperlinkedModelSerializer
from baseuser.models import BaseUsers, UserProfile, CompanyProfile


class BaseUsersSafeSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = BaseUsers
        exclude = ['django_user', 'password1', 'password2']


class BaseUsersSerializer(ModelSerializer):
    class Meta:
        model = BaseUsers
        exclude = ['django_user']
        # extra_kwargs = {'password': {'write_only': True}}


class UserProfileSerializer(ModelSerializer):
    liked_posts = serializers.HyperlinkedRelatedField(many=True,
                                                      view_name='PostLike-detail',
                                                      read_only=True)

    class Meta:
        model = UserProfile
        fields = '__all__'


class CompanyProfileSerializer(ModelSerializer):

    class Meta:
        model = CompanyProfile
        fields = '__all__'

# class SnippetSerializer(serializers.HyperlinkedModelSerializer):
#     owner = serializers.ReadOnlyField(source='owner.username')
#     highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')
#
#     class Meta:
#         model = Snippet
#         fields = ['url', 'id', 'highlight', 'owner',
#                   'title', 'code', 'linenos', 'language', 'style']
#
#
# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True)
#
#     class Meta:
#         model = User
#         fields = ['url', 'id', 'username', 'snippets']