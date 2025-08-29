from rest_framework import serializers
from djoser.serializers import UserSerializer as DjoserUserSerializer
from drf_extra_fields.fields import Base64ImageField

from .models import (
    User,
    Subscription
)


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
        fields = ("id", "email", "username", "first_name", "last_name", "avatar", "is_subscribed")

    def get_is_subscribed(self, obj):
        request = self.context.get("request")
        if not request or request.user.is_anonymous:
            return False
        return Subscription.objects.filter(user=request.user, author=obj).exists()


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
    pass
