from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Кастомная модель пользователя с логином по email"""
    username = models.CharField(
        max_length=150,
        unique=True,
        blank=True,
        null=True,
        help_text="Имя пользователя"
    )
    email = models.EmailField(
        unique=True,
        max_length=254,
        help_text="Электронная почта"
    )
    avatar = models.ImageField(
        upload_to='users/',
        blank=True,
        null=True,
        help_text="Аватар"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]


class Subscription(models.Model):
    """Модель подписки пользователя на автора"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        help_text="Пользователь, который подписывается"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="subscribers",
        help_text="Автор, на которого подписываются"
    )

    objects = models.Manager()

    class Meta:
        unique_together = ("user", "author")

    def __str__(self):
        return f"{self.user} → {self.author}"
