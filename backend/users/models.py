from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Кастомная модель пользователя с логином по email."""
    username = models.CharField(
        max_length=150,
        unique=True,
        blank=True,
        null=True,
    )
    email = models.EmailField(
        unique=True,
        max_length=254,
    )

    avatar = models.ImageField(
        upload_to='users/',
        blank=True,
        null=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
