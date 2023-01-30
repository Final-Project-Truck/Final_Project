from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from baseuser.models import BaseUsers, UserProfile, CompanyProfile


class BaseUsersSerializer(ModelSerializer):
    class Meta:
        model = BaseUsers
        exclude = ['django_user']
        extra_kwargs = {'password': {'write_only': True}}  # this works


class BaseUsersRegisterAPIView(serializers.Serializer):
    pass  # todo check whether we need this one
    # this should include the password and email validations


# class PersonBaseUsersSerializer(BaseUsersSerializer):
#     class Meta(BaseUsersSerializer.Meta):
#         fields = BaseUsersSerializer.Meta.fields + ('user_type',)
#
#     def create(self, validated_data):
#         validated_data['user_type'] = 'per'
#         return super().create(
#             validated_data)

class PersonBaseUsersSerializer(BaseUsersSerializer):
    user_type = serializers.SerializerMethodField()
    exclude = ['user_type']  # todo check whether you can exclude it from the

    # baseuserserialaizer
    def get_user_type(self, obj):
        return 'per'

    user_type = serializers.CharField(default='per', read_only=True)
    # def create(self, validated_data):
    #     validated_data['user_type'] = self.initial_data['user_type']
    #     return super().create(validated_data)


class CompanyBaseUsersSerializer(BaseUsersSerializer):
    user_type = serializers.CharField(default='com', read_only=True)

    def create(self, validated_data):
        validated_data['user_type'] = self.initial_data['user_type']
        return super().create(validated_data)


class TockenAuthenticationSerializer(ModelSerializer):
    pass


class ChangePasswordSerializer(serializers.Serializer):  # todo check the
    # underlined tipp Class ChangePasswordSerializer must implement all
    # abstract methods
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    class Meta:
        model = BaseUsers
        fields = ('password',)


class UserProfileSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class CompanyProfileSerializer(ModelSerializer):
    class Meta:
        model = CompanyProfile
        exclude = ['base_user']
