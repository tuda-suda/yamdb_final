from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register('', views.UserViewSet)

# auth_urls = [
#     path('email/', views.EmailSignUpView, name='token_obtain_pair'),
#     path('token/', views.CodeConfirmationView, name='token'),
# ]

auth_urls = [
    path('email/', views.UserCreate.as_view(), name='token_obtain_pair'),
    path('token/', views.MyTokenObtainPairView.as_view(), name='token'),
]

urlpatterns = [
    path('auth/', include(auth_urls)),
    path('users/', include(router.urls))
]
