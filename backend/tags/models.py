from django.db import models

class Tag(models.Model):
    """Модель тегов (меток) для поиска данных"""
    name = models.CharField(
        max_length=32,
        unique=True,
    )
    slug = models.SlugField(
        max_length=32,
        unique=True,
    )

    objects = models.Manager()

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name
