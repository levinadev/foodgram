from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from api.constants import (
    MAX_COOKING_TIME,
    MAX_INGREDIENT_NAME_LENGTH,
    MAX_MEASUREMENT_UNIT_LENGTH,
    MAX_RECIPE_NAME_LENGTH,
    MAX_TAG_NAME_LENGTH,
    MAX_TAG_SLUG_LENGTH,
    MIN_COOKING_TIME,
)

User = get_user_model()


class Ingredient(models.Model):
    """Модель ингредиента."""

    name = models.CharField(
        max_length=MAX_INGREDIENT_NAME_LENGTH,
        help_text="Название ингредиента, например: 'Сахар', 'Молоко'",
        verbose_name="Название ингредиента",
    )
    measurement_unit = models.CharField(
        max_length=MAX_MEASUREMENT_UNIT_LENGTH,
        help_text="Единица измерения ингредиента, например: 'г', 'мл'",
        verbose_name="Единица измерения",
    )

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.measurement_unit})"


class Tag(models.Model):
    """Модель тега для поиска данных."""

    name = models.CharField(
        max_length=MAX_TAG_NAME_LENGTH,
        unique=True,
        help_text="Название тега",
        verbose_name="Название тега",
    )
    slug = models.SlugField(
        max_length=MAX_TAG_SLUG_LENGTH,
        unique=True,
        help_text="slug тега",
        verbose_name="Slug тега",
    )

    objects = models.Manager()

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецепта."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
        help_text="Пользователь, который создал рецепт",
        verbose_name="Автор",
    )
    name = models.CharField(
        max_length=MAX_RECIPE_NAME_LENGTH,
        help_text="Название рецепта",
        verbose_name="Название рецепта",
    )
    image = models.ImageField(
        upload_to="recipes/",
        help_text="Фото блюда",
        verbose_name="Фото блюда",
    )
    text = models.TextField(
        help_text="Описание рецепта", verbose_name="Описание"
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through="RecipeIngredient",
        related_name="recipes",
        help_text="Ингредиенты",
        verbose_name="Ингредиенты",
    )
    cooking_time = models.PositiveIntegerField(
        validators=[
            MinValueValidator(
                MIN_COOKING_TIME, message="Время не может быть меньше 1 минуты"
            ),
            MaxValueValidator(
                MAX_COOKING_TIME, message="Время не может превышать 24 часа"
            ),
        ],
        help_text="Время приготовления в минутах",
        verbose_name="Время приготовления (минуты)",
    )
    tags = models.ManyToManyField(
        Tag, related_name="recipes", help_text="Тег", verbose_name="Теги"
    )

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        ordering = ["-id"]  # сначала новые записи

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    """Модель количества ингредиента в рецепте."""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        help_text="Рецепт, к которому относится ингредиент",
        verbose_name="Рецепт",
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        help_text="Ингредиент рецепта",
        verbose_name="Ингредиент",
    )
    amount = models.PositiveIntegerField(
        help_text="Количество ингредиента в рецепте",
        verbose_name="Количество",
    )

    class Meta:
        unique_together = ("recipe", "ingredient")
        verbose_name = "Ингредиент рецепта"
        verbose_name_plural = "Ингредиенты рецептов"
        ordering = ["recipe__name", "ingredient__name"]


class Favorite(models.Model):
    """Модель избранного рецепта."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text="Пользователь, добавивший рецепт в избранное",
        verbose_name="Пользователь",
    )
    recipe = models.ForeignKey(
        "Recipe",
        on_delete=models.CASCADE,
        related_name="favorites",
        help_text="Рецепт, добавленный в избранное",
        verbose_name="Рецепт",
    )

    class Meta:
        unique_together = ("user", "recipe")
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"
        ordering = ["-id"]  # сначала новые записи


class ShoppingCart(models.Model):
    """Модель корзины."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="shopping_cart",
        help_text="Пользователь, которому принадлежит список покупок",
        verbose_name="Пользователь",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="in_shopping_cart",
        help_text="Рецепт, добавленный в список покупок",
        verbose_name="Рецепт",
    )

    class Meta:
        unique_together = ("user", "recipe")
        verbose_name = "Список покупок"
        verbose_name_plural = "Списки покупок"
        ordering = ["-id"]  # сначала новые записи

    def __str__(self):
        return f"{self.user} — {self.recipe}"
