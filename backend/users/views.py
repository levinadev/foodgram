from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import (
    User,
    Subscription,
)
from .serializers import (
    AvatarSerializer,
    UserSerializer,
)


class AvatarView(generics.UpdateAPIView):
    serializer_class = AvatarSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        """Удалить аватар"""
        user = self.get_object()
        user.avatar.delete(save=True)
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubscriptionsView(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        author_ids = Subscription.objects.filter(user=user).values_list('author_id', flat=True)
        return User.objects.filter(id__in=author_ids)

    def get(self, request, *args, **kwargs):
        """Получить список подписок"""
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, id, *args, **kwargs):
        """Подписка на пользователя"""
        author = get_object_or_404(User, id=id)
        Subscription.objects.get_or_create(user=request.user, author=author)
        serializer = UserSerializer(author, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, id, *args, **kwargs):
        """Отписка от пользователя"""
        author = get_object_or_404(User, id=id)
        deleted, _ = Subscription.objects.filter(user=request.user, author=author).delete()
        if deleted == 0:
            return Response({"detail": "Вы не были подписаны"}, status=400)
        serializer = UserSerializer(author, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
