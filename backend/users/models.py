from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from common.constants import (
    MAX_EMAIL_LENGTH,
    MAX_NAME_LENGTH,
    MAX_USERNAME_LENGTH,
)


class UserManager(BaseUserManager):
    """Менеджер пользователей с авторизацией по email."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email обязателен")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Суперпользователь должен иметь is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(
                "Суперпользователь должен иметь is_superuser=True."
            )

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Кастомная модель пользователя с логином по email."""

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        max_length=MAX_USERNAME_LENGTH,
        unique=True,
        help_text="Имя пользователя",
        verbose_name="Имя пользователя",
        validators=[username_validator],
    )
    email = models.EmailField(
        unique=True,
        max_length=MAX_EMAIL_LENGTH,
        help_text="Электронная почта",
        verbose_name="Электронная почта",
    )
    first_name = models.CharField(
        max_length=MAX_NAME_LENGTH,
        blank=False,
        help_text="Имя",
        verbose_name="Имя",
    )
    last_name = models.CharField(
        max_length=MAX_NAME_LENGTH,
        blank=False,
        help_text="Фамилия",
        verbose_name="Фамилия",
    )
    avatar = models.ImageField(
        upload_to="users/",
        blank=True,
        null=True,
        help_text="Аватар",
        verbose_name="Аватар",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["username"]

    def __str__(self):
        return self.email


class Subscription(models.Model):
    """Модель подписки пользователя на автора."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        help_text="Пользователь, который подписывается",
        verbose_name="Пользователь",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="subscribers",
        help_text="Автор, на которого подписываются",
        verbose_name="Автор",
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        ordering = ["user__username", "author__username"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "author"], name="unique_subscription"
            )
        ]

    def __str__(self):
        return f"{self.user} → {self.author}"
