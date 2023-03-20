from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели User."""
    email = serializers.EmailField(max_length=254, required=True)
    username = serializers.SlugField(max_length=50, required=True)

    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        model = User
        read_only_field = ('role',)

    def validate(self, data):
        email = data.get('email')
        username = data.get('username')
        if (not User.objects.filter(email=email).exists()
                and User.objects.filter(username=username).exists()):
            raise serializers.ValidationError(
                'Пользователь с этой почтой уже существует.'
            )
        if (User.objects.filter(email=email).exists()
                and not User.objects.filter(username=username).exists()):
            raise serializers.ValidationError(
                'Пользователь с этой почтой уже существует.'
            )
        if username == 'me':
            raise serializers.ValidationError(
                'Нельзя использовать "me" как имя.'
            )
        return data


class JWTSerializer(serializers.Serializer):
    """Сериализатор запроса JWT токена."""
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)


class CategorySerializer(serializers.ModelSerializer):
    """Класс сериализатор категории."""

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Класс сериализатор жанра."""

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleReadSerializer(serializers.ModelSerializer):
    """Класс сериализатор получения списка произведений."""
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(
        many=True,
        required=False,
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )
        model = Title


class TitleWriteSerializer(serializers.ModelSerializer):
    """Класс сериализатор создания произведений."""
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category'
        )
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор модели отзывов."""
    author = serializers.StringRelatedField(read_only=True,)

    class Meta:
        fields = ('id', 'title', 'author', 'text', 'score', 'pub_date')
        read_only_fields = ('title',)
        model = Review

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data
        user = self.context['request'].user
        title_id = self.context['view'].kwargs.get('title_id')
        if Review.objects.filter(author=user, title_id=title_id).exists():
            raise serializers.ValidationError(
                'Отзыв уже оставлен!'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    '''Сериалайзер комментариев.'''
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        fields = ('id', 'review', 'author', 'text', 'pub_date')
        read_only_fields = ('review',)
        model = Comment
