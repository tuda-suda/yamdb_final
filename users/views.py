from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from api_yamdb.settings import YAMDB_NOREPLY_EMAIL

from .models import User
from .permissions import IsAdmin
from .serializers import (CodeConfirmationSerializer, EmailSignUpSerializer,
                          UserSerializer)


class EmailSignUpView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = EmailSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        new_user = None
        if not User.objects.filter(email=email).exists():
            new_user = User.objects.create_user(email=email, is_active=False)

        user = new_user or get_object_or_404(User, email=email)
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='Код подтверждения',
            message=f'Ваш код подтверждения {confirmation_code}',
            from_email=YAMDB_NOREPLY_EMAIL,
            recipient_list=[email]
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class CodeConfirmationView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = CodeConfirmationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        confirmation_code = serializer.data.get('confirmation_code')
        user = get_object_or_404(User, email=email)

        if default_token_generator.check_token(user, confirmation_code):
            token = AccessToken.for_user(user)
            return Response(
                {'token': token},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (IsAdmin,)

    @action(
        methods=['get', 'patch'],
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        user = request.user
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)

        serializer = self.get_serializer(user)
        return Response(serializer.data)
