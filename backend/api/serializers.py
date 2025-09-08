import logging

from django.contrib.auth.validators import UnicodeUsernameValidator
from djoser.serializers import (
    UserCreateSerializer as DjoserUserCreateSerializer,
)
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from recipes.models import (
    Ingredient,
    Recipe,
    RecipeIngredient,
    Tag,
)
from users.models import Subscription, User

from .constants import (
    MAX_COOKING_TIME,
    MAX_INGREDIENT_AMOUNT,
    MAX_NAME_LENGTH,
    MAX_USERNAME_LENGTH,
    MIN_COOKING_TIME,
    MIN_INGREDIENT_AMOUNT,
)

logger = logging.getLogger(__name__)


class BaseUserSerializer(serializers.ModelSerializer):
    """Базовый сериализатор пользователя."""

    avatar = Base64ImageField(required=False)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "avatar",
            "is_subscribed",
        )

    def get_is_subscribed(self, obj):
        request = self.context.get("request")
        user = getattr(request, "user", None)
        if not user or not user.is_authenticated:
            return False
        return Subscription.objects.filter(user=user, author=obj).exists()


class ShortUserSerializer(BaseUserSerializer):
    """Короткий сериализатор для вложения автора в рецептах."""

    avatar = serializers.SerializerMethodField()

    class Meta(BaseUserSerializer.Meta):
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_subscribed",
            "avatar",
        )

    def get_avatar(self, obj):
        request = self.context.get("request")
        if obj.avatar:
            return request.build_absolute_uri(obj.avatar.url)
        return None


class UserCreateSerializer(DjoserUserCreateSerializer):
    """Сериализатор для регистрации пользователей (Djoser)."""

    first_name = serializers.CharField(
        required=True, max_length=MAX_NAME_LENGTH
    )
    last_name = serializers.CharField(
        required=True, max_length=MAX_NAME_LENGTH
    )
    username = serializers.CharField(
        required=True,
        max_length=MAX_USERNAME_LENGTH,
        validators=[UnicodeUsernameValidator()],
    )

    class Meta(DjoserUserCreateSerializer.Meta):
        model = User
        fields = DjoserUserCreateSerializer.Meta.fields + (
            "first_name",
            "last_name",
            "username",
        )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name", "slug"]


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов для рецепта."""

    id = serializers.ReadOnlyField(source="ingredient.id")
    name = serializers.ReadOnlyField(source="ingredient.name")
    measurement_unit = serializers.ReadOnlyField(
        source="ingredient.measurement_unit"
    )

    class Meta:
        model = RecipeIngredient
        fields = ["id", "name", "measurement_unit", "amount"]


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения рецепта."""

    ingredients = RecipeIngredientSerializer(
        many=True, read_only=True, source="recipe_ingredients"
    )
    tags = TagSerializer(many=True)
    author = ShortUserSerializer()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = [
            "id",
            "tags",
            "author",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time",
        ]

    def get_is_favorited(self, obj):
        """True, если рецепт в избранном у пользователя."""
        user = getattr(self.context.get("request"), "user", None)
        return (
            user
            and user.is_authenticated
            and obj.in_favorites.filter(user=user).exists()
        )

    def get_is_in_shopping_cart(self, obj):
        """True, если рецепт в корзине у пользователя."""
        user = getattr(self.context.get("request"), "user", None)
        return (
            user
            and user.is_authenticated
            and obj.in_shopping_cart.filter(user=user).exists()
        )


class RecipeIngredientWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для ингредиентов при создании рецепта."""

    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField()

    class Meta:
        model = RecipeIngredient
        fields = ("id", "amount")

    def validate_amount(self, value):
        if value < MIN_INGREDIENT_AMOUNT:
            raise serializers.ValidationError(
                f"Количество должно быть не меньше {MIN_INGREDIENT_AMOUNT}."
            )
        if value > MAX_INGREDIENT_AMOUNT:
            raise serializers.ValidationError(
                f"Количество не может превышать {MAX_INGREDIENT_AMOUNT}."
            )
        return value


class ShortRecipeSerializer(serializers.ModelSerializer):
    """Короткий сериализатор для избранного/корзины."""

    class Meta:
        model = Recipe
        fields = ["id", "name", "image", "cooking_time"]


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания/обновления рецепта."""

    ingredients = RecipeIngredientWriteSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
    image = Base64ImageField(required=True)
    cooking_time = serializers.IntegerField(
        min_value=MIN_COOKING_TIME,
        max_value=MAX_COOKING_TIME,
        error_messages={
            "min_value": f"Мин. время: {MIN_COOKING_TIME} мин",
            "max_value": f"Макс. время: {MAX_COOKING_TIME} мин",
        },
    )

    class Meta:
        model = Recipe
        fields = [
            "ingredients",
            "tags",
            "image",
            "name",
            "text",
            "cooking_time",
        ]

    def validate_image(self, value):
        if self.instance is None and not value:
            raise serializers.ValidationError(
                "Картинка обязательна для рецепта."
            )
        if value in ("", None):
            raise serializers.ValidationError(
                "Поле image не может быть пустым."
            )
        return value

    def validate(self, data):
        ingredients = data.get("ingredients")
        tags = data.get("tags")

        if not ingredients:
            raise serializers.ValidationError(
                {"ingredients": "Нельзя создать рецепт без ингредиентов."}
            )

        ingredient_ids = [item["id"] for item in ingredients]
        if len(ingredient_ids) != len(set(ingredient_ids)):
            raise serializers.ValidationError(
                {"ingredients": "Ингредиенты не должны повторяться."}
            )

        if not tags:
            raise serializers.ValidationError(
                {"tags": "Нельзя создать рецепт без тегов."}
            )

        tag_ids = [tag.id for tag in tags]
        if len(tag_ids) != len(set(tag_ids)):
            raise serializers.ValidationError(
                {"tags": "Теги не должны повторяться."}
            )

        return data

    def _create_ingredients(self, recipe, ingredients_data):
        recipe_ingredients = [
            RecipeIngredient(
                recipe=recipe,
                ingredient=ingredient["id"],
                amount=ingredient["amount"],
            )
            for ingredient in ingredients_data
        ]
        RecipeIngredient.objects.bulk_create(recipe_ingredients)

    def create(self, validated_data):
        ingredients_data = validated_data.pop("ingredients")
        tags = validated_data.pop("tags")
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)

        self._create_ingredients(recipe, ingredients_data)
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop("ingredients", None)
        tags = validated_data.pop("tags", None)

        instance = super().update(instance, validated_data)

        if tags is not None:
            instance.tags.set(tags)

        if ingredients_data is not None:
            instance.recipe_ingredients.all().delete()
            self._create_ingredients(instance, ingredients_data)

        return instance

    def to_representation(self, instance):
        """После создания/обновления возвращаем нормальный RecipeSerializer."""
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


class SubscriptionUserSerializer(BaseUserSerializer):
    """Сериализатор для подписок / me, возвращает рецепты."""

    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()

    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = BaseUserSerializer.Meta.fields + (
            "recipes",
            "recipes_count",
            "avatar",
        )

    def get_avatar(self, obj):
        request = self.context.get("request")
        if obj.avatar:
            return request.build_absolute_uri(obj.avatar.url)
        return None

    def get_recipes(self, obj):
        request = self.context.get("request")
        recipes_qs = obj.recipes.all()
        if request:
            limit = request.query_params.get("recipes_limit")
            if limit and limit.isdigit():
                recipes_qs = recipes_qs[: int(limit)]
        return ShortRecipeSerializer(
            recipes_qs, many=True, context=self.context
        ).data

    def get_recipes_count(self, obj):
        return obj.recipes.count()
