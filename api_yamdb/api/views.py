from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg, F
from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Genre, Review, Title
from users.models import User

from .filters import TitleFilter
from .mixins import UpdateModelMixin, CreateListDestroyViewSet
from .permissions import IsAdmin, IsAdminOrReadOnly, IsOwnerOrStaffOrReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, JWTSerializer, ReviewSerializer,
                          TitleReadSerializer, TitleWriteSerializer,
                          UserSerializer)


@api_view(['POST'])
@permission_classes((AllowAny,))
def signup(request):
    """
    Запрос регистрации нового пользователя.
    Создаёт нового пользователя, если он не был создан ранее администратором.
    Отправляет код подтверждения на email пользователя.
    """
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data.get('email')
    username = serializer.validated_data.get('username')
    if (not User.objects.filter(email=email).exists()
            and not User.objects.filter(username=username).exists()):
        User.objects.create(username=username, email=email)
    user = User.objects.filter(email=email).first()
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        'Код подтверждения Yamdb',
        f'Ваш код подтверждения: {confirmation_code}',
        settings.DEFAULT_FROM_EMAIL,
        [email]
    )
    return Response(
        {'email': str(email), 'username': str(username)},
        status=HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes((AllowAny,))
def token(request):
    """
    Запрос на получение JWT токена.
    Для получения необходим корректный confirmation code.
    """
    serializer = JWTSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    confirmation_code = serializer.validated_data.get(
        'confirmation_code'
    )
    user = get_object_or_404(User, username=username)
    if default_token_generator.check_token(user, confirmation_code):
        token = AccessToken.for_user(user)
        return Response(
            {'token': str(token)}, status=HTTP_200_OK
        )
    return Response(
        {'confirmation_code': 'Неверный код подтверждения!'},
        status=HTTP_400_BAD_REQUEST
    )


class UserViewSet(CreateListDestroyViewSet,
                  UpdateModelMixin,
                  RetrieveModelMixin):
    """Просмотр и редактирование пользователей."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (IsAdmin,)
    filter_backends = [filters.SearchFilter]
    search_fields = ('=username',)

    @action(detail=False,
            methods=['patch', 'get'],
            permission_classes=[IsAuthenticated])
    def me(self, request):
        user = self.request.user
        serializer = self.get_serializer(user)
        if self.request.method == 'PATCH':
            serializer = self.get_serializer(
                user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=user.role)
        return Response(serializer.data)


class CategoryViewSet(CreateListDestroyViewSet):
    """Просмотр и редактирование категорий."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = [SearchFilter]
    lookup_field = 'slug'
    search_fields = ('=name',)


class GenreViewSet(CreateListDestroyViewSet):
    """Просмотр и редактирование жанров."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    lookup_field = 'slug'
    search_fields = ('=name',)


class TitleViewSet(viewsets.ModelViewSet):
    """Просмотр и редактирование названий."""
    queryset = Title.objects.annotate(
        rating=Avg(F('review__score'))
    )
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Просмотр и редактирование рецензий."""
    serializer_class = ReviewSerializer
    permission_classes = (IsOwnerOrStaffOrReadOnly,)
    ordering = ('-pub_date')

    def get_title(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title

    def get_queryset(self):
        title = ReviewViewSet.get_title(self)
        new_queryset = title.review.all()
        return new_queryset

    def perform_create(self, serializer):
        title = ReviewViewSet.get_title(self)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Просмотр и редактирование комментариев."""
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerOrStaffOrReadOnly,)
    ordering = ('-pub_date')

    def get_review(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        return review

    def get_queryset(self):
        review = CommentViewSet.get_review(self)
        new_queryset = review.comments.all()
        return new_queryset

    def perform_create(self, serializer):
        review = CommentViewSet.get_review(self)
        serializer.save(author=self.request.user, review=review)
