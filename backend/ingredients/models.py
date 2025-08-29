from django.db import models


class Ingredient(models.Model):
    """Модель ингредиента"""
    name = models.CharField(
        max_length=128,
        help_text="Название ингредиента, например: 'Сахар', 'Молоко'"
    )
    measurement_unit = models.CharField(
        max_length=32,
        help_text="Единица измерения ингредиента, например: 'г', 'мл'"
    )

    def __str__(self):
        return f"{self.name} ({self.measurement_unit})"
