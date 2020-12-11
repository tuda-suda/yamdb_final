from rest_framework import serializers

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
