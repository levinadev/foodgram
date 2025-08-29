from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from users.serializers import ShortUserSerializer
from tags.serializers import TagSerializer

from .models import Recipe, RecipeIngredient
from tags.models import Tag
from ingredients.models import Ingredient


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


class RecipeIngredientWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для ингредиентов при создании рецепта"""
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all()
    )
    amount = serializers.IntegerField()

    class Meta:
        model = RecipeIngredient
        fields = ("id", "amount")


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания/обновления рецепта"""
    ingredients = RecipeIngredientWriteSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = [
            "ingredients", "tags", "image",
            "name", "text", "cooking_time"
        ]

    def create(self, validated_data):
        ingredients_data = validated_data.pop("ingredients")
        tags = validated_data.pop("tags")
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)

        # создаем ингредиенты
        for ingredient in ingredients_data:
            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient=ingredient["id"],
                amount=ingredient["amount"]
            )
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop("ingredients")
        tags = validated_data.pop("tags")

        instance.name = validated_data.get("name", instance.name)
        instance.text = validated_data.get("text", instance.text)
        instance.cooking_time = validated_data.get("cooking_time", instance.cooking_time)
        if "image" in validated_data:
            instance.image = validated_data["image"]
        instance.save()

        # обновляем теги
        instance.tags.set(tags)

        # обновляем ингредиенты
        instance.recipeingredient_set.all().delete()
        for ingredient in ingredients_data:
            RecipeIngredient.objects.create(
                recipe=instance,
                ingredient=ingredient["id"],
                amount=ingredient["amount"]
            )

        return instance

    def to_representation(self, instance):
        """После создания/обновления возвращаем нормальный RecipeSerializer"""
        return RecipeSerializer(instance, context=self.context).data
