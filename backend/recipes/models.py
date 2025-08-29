from django.db import models

from tags.models import Tag
from ingredients.models import Ingredient

from django.conf import settings


class Recipe(models.Model):
    """Модель рецепта"""
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
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


class Favorite(models.Model):
    """Избранные рецепты"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        help_text="Пользователь, добавивший рецепт в избранное"
    )
    recipe = models.ForeignKey(
        "Recipe",
        on_delete=models.CASCADE,
        related_name="favorites",
        help_text="Рецепт, добавленный в избранное"
    )

    class Meta:
        unique_together = ("user", "recipe")
