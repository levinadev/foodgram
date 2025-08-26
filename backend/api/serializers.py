from rest_framework import serializers
from djoser.serializers import UserSerializer as DjoserUserSerializer
from drf_extra_fields.fields import Base64ImageField
from users.models import User


class AvatarSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField()

    class Meta:
        model = User
        fields = ("avatar",)


class UserSerializer(DjoserUserSerializer):
    avatar = Base64ImageField(required=False)
    is_subscribed = serializers.SerializerMethodField()

    class Meta(DjoserUserSerializer.Meta):
        model = User
        fields = DjoserUserSerializer.Meta.fields + (
            "first_name",
            "last_name",
            "avatar",
            "is_subscribed",
        )

    def get_is_subscribed(self, obj):
        # TODO добавить логику подписки позже
        return False
