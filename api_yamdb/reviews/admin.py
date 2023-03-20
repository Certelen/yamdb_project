from django.contrib import admin
from users.models import User

from .models import Category, Comment, Genre, Review, Title


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Регистрация модели Category в панели суперпользователя"""
    list_display = ('id', 'name', 'slug',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Регистрация модели Genre в панели суперпользователя"""
    list_display = ('id', 'name', 'slug',)


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """Регистрация модели Title в панели суперпользователя"""
    list_display = ('id', 'name', 'year', 'category',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Регистрация модели User в панели суперпользователя"""
    list_display = (
        'id',
        'username',
        'email',
        'role',
        'bio',
        'first_name',
        'last_name',
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Регистрация модели Review в панели суперпользователя"""
    list_display = ('id', 'title_id', 'text', 'author', 'pub_date',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Регистрация модели Comment в панели суперпользователя"""
    list_display = ('id', 'review_id', 'text', 'author', 'pub_date',)
