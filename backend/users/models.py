from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

from api.constants import MAX_EMAIL_LENGTH, MAX_USERNAME_LENGTH


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

    username = models.CharField(
        max_length=MAX_USERNAME_LENGTH,
        unique=True,
        blank=True,
        null=True,
        help_text="Имя пользователя",
        verbose_name="Имя пользователя",
    )
    email = models.EmailField(
        unique=True,
        max_length=MAX_EMAIL_LENGTH,
        help_text="Электронная почта",
        verbose_name="Электронная почта",
    )
    avatar = models.ImageField(
        upload_to="users/",
        blank=True,
        null=True,
        help_text="Аватар",
        verbose_name="Аватар",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

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

    objects = models.Manager()

    class Meta:
        unique_together = ("user", "author")
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self):
        return f"{self.user} → {self.author}"
