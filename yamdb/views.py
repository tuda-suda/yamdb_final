from django.contrib.auth import get_user_model
from django.db.models import Avg
from rest_framework import filters, generics, mixins, permissions, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.permissions import IsAdmin, ReadOnly, IsOwner, IsModerator

from .filters import TitleFilter
from .models import Category, Genre, Title, Review
from .serializers import (CategorySerializer, GenreSerializer, TitleSerializer, 
    ReviewSerializer, CommentSerializer)

User = get_user_model()


class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdmin | ReadOnly]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdmin | ReadOnly]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
    serializer_class = TitleSerializer
    permission_classes = [IsAdmin | ReadOnly]
    filterset_class = TitleFilter


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update']:
            self.permission_classes = [IsOwner, ]
        elif self.action in ['destroy', ]:
            self.permission_classes = [IsOwner | IsAdmin | IsModerator]
        elif self.action in ['create']:
            self.permission_classes = [IsAuthenticated, ]
        elif self.action in ['list']:
            self.permission_classes = [AllowAny, ]
        return super().get_permissions()

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        reviews = Review.objects.filter(title__id=title.pk,
                                       author=self.request.user)
        if reviews:
            raise ValidationError(f'You have already reviewed this title.')
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update']:
            self.permission_classes = [IsOwner, ]
        elif self.action in ['destroy', ]:
            self.permission_classes = [IsOwner | IsAdmin | IsModerator]
        elif self.action in ['create']:
            self.permission_classes = [IsAuthenticated, ]
        elif self.action in ['list']:
            self.permission_classes = [AllowAny, ]
        return super().get_permissions()

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id, title__pk=title_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'),
                                   title__pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, review=review)
