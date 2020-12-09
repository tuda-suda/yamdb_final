from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User


class EmailSignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class CodeConfirmationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    confirmation_code = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
           'first_name', 'last_name', 'username', 'bio', 'email', 'role'
        )
        required_fields = ('username', 'email')


class YamdbTokenObtainPairSerializer(TokenObtainPairSerializer):
    username = None
    password = None
    email = serializers.CharField(
        max_length=None,
        min_length=None,
        allow_blank=False,
        write_only=True
    )
    confirmation_code = serializers.CharField(
        allow_blank=False,
        write_only=True
    )
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ('confirmation_code', 'email',)
