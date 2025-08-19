from rest_framework import serializers
from users.models import User


class UserListSerializer(serializers.ModelSerializer):
    """Сериализатор для вывода списка пользователей."""

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name']
