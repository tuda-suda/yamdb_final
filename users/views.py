from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, status, viewsets, filters
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.pagination import PageNumberPagination

from api_yamdb.settings import YAMDB_NOREPLY_EMAIL

from .models import User
from .permissions import IsAdmin, IsModerator, IsOwner, ReadOnly
from .serializers import (CodeConfirmationSerializer, EmailSignUpSerializer,
    UserSerializer, YamdbTokenObtainPairSerializer)


# class EmailSignUpView(APIView):
#     permission_classes = (AllowAny,)
    
#     def post(self, request):
#         serializer = EmailSignUpSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         email = serializer.data.get('email')
#         new_user = None
#         if not User.objects.filter(email=email).exists():
#             new_user = User.objects.create_user(email=email, is_active=False)
        
#         user = new_user or get_object_or_404(User, email=email)
#         confirmation_code = default_token_generator.make_token(user)
#         send_mail(
#             subject='Код подтверждения',
#             message=f'Ваш код подтверждения {confirmation_code}',
#             from_email=YAMDB_NOREPLY_EMAIL,
#             recipient_list=[email]
#         )
#         return Response(serializer.data, status=status.HTTP_200_OK)


# class CodeConfirmationView(APIView):
#     permission_classes = (AllowAny,)

#     def post(self, request):
#         serializer = CodeConfirmationSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         email = serializer.data.get('email')
#         confirmation_code = serializer.data.get('confirmation_code')
#         user = get_object_or_404(User, email=email)

#         if default_token_generator.check_token(user, confirmation_code):
#             token = AccessToken.for_user(user)
#             return Response(
#                 {'token': token},
#                 status=status.HTTP_200_OK
#             )
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserCreate(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        serializer = UserSerializer(data=self.request.data)
        user = User.objects.get_or_create(
                email=self.request.user.email,
                username=self.request.user.username,
                password='')
        user_email = user.email
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='Yours confirmation code',
            message=f'confirmation_code: {confirmation_code}',
            from_email='registration@yamdb.fake',
            recipient_list=(user_email,),
            fail_silently=False
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = YamdbTokenObtainPairSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=username',)
    pagination_class = PageNumberPagination

    @action(
        methods=('get', 'patch'), detail=False,
        permission_classes=(IsAuthenticated,),
    )
    def me(self, request):
        user_profile = request.user
        if request.method == 'GET':
            serializer = UserSerializer(user_profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(
            user_profile, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     lookup_field = 'username'
#     permission_classes = (IsAdmin,)

#     @action(
#         methods=['get', 'patch'], 
#         detail=False, 
#         permission_classes=[IsAuthenticated]
#     )
#     def me(self, request):
#         user = request.user
#         if request.method == 'PATCH':
#             serializer = self.get_serializer(
#                 user, 
#                 data=request.data, 
#                 partial=True
#             )
#             serializer.is_valid(raise_exception=True)
#             self.perform_update(serializer)
#             return Response(serializer.data)
          
#         serializer = self.get_serializer(user)
#         return Response(serializer.data)

