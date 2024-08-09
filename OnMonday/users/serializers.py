from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import User, UserEvents

# User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'phone', 'email', 'gender', 'date_birth', 'hobby', 'country')


class GoogleLoginSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()
    user_id = serializers.IntegerField()
    username = serializers.CharField()
    email = serializers.EmailField()
    phone = serializers.CharField()


class UserEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEvents
        fields = ('name', 'date', 'counter_users')

