from django.db import models


class Tag(models.Model):
    """Модель тега для поиска данных"""
    name = models.CharField(
        max_length=32,
        unique=True,
        help_text="Название тега"
    )
    slug = models.SlugField(
        max_length=32,
        unique=True,
        help_text="slug тега"
    )

    objects = models.Manager()

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name
