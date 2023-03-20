from django.contrib.auth.models import AbstractUser
from django.db import models


class Roles(models.TextChoices):
    """
    Модель роли.
    Возможные роли: пользователь, модератор, администратор.
    """
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'


class User(AbstractUser):
    """
    Дополняется модель пользователя.
    Новым пользователям по умолчанию присваивается роль юзер.
    """
    email = models.EmailField(
        'Почта пользователя',
        unique=True,
        max_length=254,
    )

    bio = models.TextField(
        'Биография',
        blank=True,
    )

    role = models.CharField(
        'Роль пользователя',
        max_length=50,
        choices=Roles.choices,
        default=Roles.USER,
    )

    @property
    def is_admin(self):
        return (
            self.role == Roles.ADMIN
            or self.is_staff
        )

    @property
    def is_moderator(self):
        return (
            self.role == Roles.MODERATOR
        )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
