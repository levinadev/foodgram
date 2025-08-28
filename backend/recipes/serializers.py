from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from users.serializers import ShortUserSerializer
from tags.serializers import TagSerializer

from .models import Recipe, Ingredient, RecipeIngredient


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов для рецепта"""
    id = serializers.ReadOnlyField(source="ingredient.id")
    name = serializers.ReadOnlyField(source="ingredient.name")
    measurement_unit = serializers.ReadOnlyField(source="ingredient.measurement_unit")

    class Meta:
        model = RecipeIngredient
        fields = ["id", "name", "measurement_unit", "amount"]


class RecipeSerializer(serializers.ModelSerializer):
    """Основной сериализатор рецепта"""
    ingredients = RecipeIngredientSerializer(source="recipeingredient_set", many=True)
    tags = TagSerializer(many=True)
    author = ShortUserSerializer()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = [
            "id", "tags", "author", "ingredients",
            "is_favorited", "is_in_shopping_cart",
            "name", "image", "text", "cooking_time"
        ]

    def get_is_favorited(self, obj):
        # TODO: временно всегда возвращаем False
        return False

    def get_is_in_shopping_cart(self, obj):
        # TODO: временно всегда возвращаем False
        return False
