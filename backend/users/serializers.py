from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from .models import Subscription, User


class AvatarSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField()

    class Meta:
        model = User
        fields = ("avatar",)


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
