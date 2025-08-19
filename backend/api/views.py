from rest_framework import generics
from users.models import User
from .serializers import UserListSerializer


class UserListView(generics.ListAPIView):
    """
    GET /users/ — вывод списка всех пользователей.
    """
    queryset = User.objects.all()
    serializer_class = UserListSerializer
