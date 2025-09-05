from django.conf import settings
from django.db import models


class Ingredient(models.Model):
    """Модель ингредиента"""

    name = models.CharField(
        max_length=128,
        help_text="Название ингредиента, например: 'Сахар', 'Молоко'",
    )
    measurement_unit = models.CharField(
        max_length=32,
        help_text="Единица измерения ингредиента, например: 'г', 'мл'",
    )

    def __str__(self):
        return f"{self.name} ({self.measurement_unit})"


class Tag(models.Model):
    """Модель тега для поиска данных"""

    name = models.CharField(
        max_length=32, unique=True, help_text="Название тега"
    )
    slug = models.SlugField(max_length=32, unique=True, help_text="slug тега")

    objects = models.Manager()

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецепта"""

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="recipes",
        help_text="Пользователь, который создал рецепт",
    )
    name = models.CharField(max_length=200, help_text="Название рецепта")
    image = models.ImageField(upload_to="recipes/", help_text="Фото блюда")
    text = models.TextField(help_text="Описание рецепта")
    ingredients = models.ManyToManyField(
        Ingredient,
        through="RecipeIngredient",
        related_name="recipes",
        help_text="Ингредиенты",
    )
    cooking_time = models.PositiveIntegerField(
        help_text="Время приготовления в минутах"
    )
    tags = models.ManyToManyField(Tag, related_name="recipes", help_text="Тег")

    objects = models.Manager()

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    """Модель количества ингредиента в рецепте"""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        help_text="Рецепт, к которому относится ингредиент",
    )
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, help_text="Ингредиент рецепта"
    )
    amount = models.PositiveIntegerField(
        help_text="Количество ингредиента в рецепте"
    )

    class Meta:
        unique_together = ("recipe", "ingredient")


class Favorite(models.Model):
    """Модель избранного рецепта"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        help_text="Пользователь, добавивший рецепт в избранное",
    )
    recipe = models.ForeignKey(
        "Recipe",
        on_delete=models.CASCADE,
        related_name="favorites",
        help_text="Рецепт, добавленный в избранное",
    )

    class Meta:
        unique_together = ("user", "recipe")


class ShoppingCart(models.Model):
    """Модель корзины"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="shopping_cart",
        help_text="Пользователь, которому принадлежит список покупок",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="in_shopping_cart",
        help_text="Рецепт, добавленный в список покупок",
    )

    class Meta:
        unique_together = ("user", "recipe")

    def __str__(self):
        return f"{self.user} — {self.recipe}"
