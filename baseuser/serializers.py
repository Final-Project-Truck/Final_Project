from rest_framework.serializers import ModelSerializer

from baseuser.models import BaseUser
from baseuser.models import Profile


class BaseUsersSafeSerializer(ModelSerializer):
    class Meta:
        model = BaseUser
        exclude = ['django_user', 'password1', 'password2']


class BaseUsersSerializer(ModelSerializer):
    class Meta:
        model = BaseUser
        exclude = ['django_user']
        # extra_kwargs = {'password': {'write_only': True}}


class ProfileSerializer(ModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'
