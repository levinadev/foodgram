import logging

from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from recipes.models import (
    Favorite, Recipe, RecipeIngredient,
    ShoppingCart, Ingredient, Tag
)

from users.models import (
    Subscription, User
)

logger = logging.getLogger(__name__)


class BaseUserSerializer(serializers.ModelSerializer):
    """Базовый сериализатор пользователя"""
    avatar = Base64ImageField(required=False)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id", "email", "username", "first_name",
            "last_name", "avatar", "is_subscribed"
        )

    def get_is_subscribed(self, obj):
        request = self.context.get("request")
        if not request or request.user.is_anonymous:
            return False
        return Subscription.objects.filter(
            user=request.user,
            author=obj
        ).exists()


class ShortUserSerializer(BaseUserSerializer):
    """Сериализатор для получения всех рецептов без списка рецептов"""
    is_subscribed = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()  # 🔹 добавляем

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_subscribed",
            "avatar",
            "full_name",
        )

    def get_is_subscribed(self, obj):
        user = self.context["request"].user
        if user.is_anonymous:
            return False
        return Subscription.objects.filter(user=user, author=obj).exists()

    def get_avatar(self, obj):
        request = self.context["request"]
        if obj.avatar:
            return request.build_absolute_uri(obj.avatar.url)
        return None

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()


class UserSerializer(BaseUserSerializer):
    """Сериализатор для подписок"""
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta(BaseUserSerializer.Meta):
        fields = BaseUserSerializer.Meta.fields + ("recipes", "recipes_count",)

    def get_recipes(self, obj):
        recipes = obj.recipes.all()[:3]
        return [
            {
                "id": r.id,
                "name": r.name,
                "image": r.image.url if r.image else None,
                "cooking_time": r.cooking_time
            }
            for r in recipes
        ]

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name", "slug"]


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов для рецепта"""
    id = serializers.ReadOnlyField(source="ingredient.id")
    name = serializers.ReadOnlyField(source="ingredient.name")
    measurement_unit = serializers.ReadOnlyField(
        source="ingredient.measurement_unit"
    )

    class Meta:
        model = RecipeIngredient
        fields = ["id", "name", "measurement_unit", "amount"]


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения рецепта"""
    ingredients = RecipeIngredientSerializer(
        source="recipeingredient_set",
        many=True
    )
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
        """True, если рецепт в избранном у пользователя"""
        user = self.context["request"].user
        if user.is_anonymous:
            return False
        return Favorite.objects.filter(user=user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        """True, если рецепт в корзине у пользователя"""
        user = self.context["request"].user
        if user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(user=user, recipe=obj).exists()


class RecipeIngredientWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для ингредиентов при создании рецепта"""
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all()
    )
    amount = serializers.IntegerField()

    class Meta:
        model = RecipeIngredient
        fields = ("id", "amount")


class ShortRecipeSerializer(serializers.ModelSerializer):
    """Короткий сериализатор для избранного/корзины"""

    class Meta:
        model = Recipe
        fields = ["id", "name", "image", "cooking_time"]


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания/обновления рецепта"""
    ingredients = RecipeIngredientWriteSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
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
        instance.cooking_time = validated_data.get(
            "cooking_time",
            instance.cooking_time
        )
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


class AvatarSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField()

    class Meta:
        model = User
        fields = ("avatar",)


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ["id", "name", "measurement_unit"]