from django.db import models
from tags.models import Tag
from users.models import User


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


class Recipe(models.Model):
    """Модель рецепта"""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
        help_text="Пользователь, который создал рецепт"
    )
    name = models.CharField(
        max_length=200,
        help_text="Название рецепта"
    )
    image = models.ImageField(
        upload_to="recipes/images/",
        help_text="Фото блюда"
    )
    text = models.TextField(
        help_text="Описание рецепта"
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through="RecipeIngredient",
        related_name="recipes",
        help_text="Ингредиенты"
    )
    cooking_time = models.PositiveIntegerField(
        help_text="Время приготовления в минутах"
    )
    tags = models.ManyToManyField(
        Tag,
        related_name="recipes",
        help_text="Тег"
    )

    objects = models.Manager()

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    """Количество ингредиента в рецепте"""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        help_text="Рецепт, к которому относится ингредиент"
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        help_text="Ингредиент рецепта"
    )
    amount = models.PositiveIntegerField(
        help_text="Количество ингредиента в рецепте"
    )

    class Meta:
        unique_together = ("recipe", "ingredient")
