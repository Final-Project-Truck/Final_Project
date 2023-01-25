from django.contrib.auth.models import User
from rest_framework import serializers
from chat.models import Message


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(many=False, slug_field='username',
                                          queryset=User.objects.all())
    receiver = serializers.SlugRelatedField(many=False, slug_field='username',
                                            queryset=User.objects.all())

    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'message', 'timestamp']

    def create(self, validated_data):
        validated_data['sender'] = self.context['request'].user
        return super().create(validated_data)


class ChatSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(many=False, slug_field='username',
                                          queryset=User.objects.all())
    receiver = serializers.SlugRelatedField(many=False, slug_field='username',
                                            queryset=User.objects.all())

    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'message', 'timestamp']
