from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import (
    User,
    Subscription,
)
from .serializers import (
    AvatarSerializer,
    UserSerializer,
)


class AvatarUpdateView(generics.UpdateAPIView):
    serializer_class = AvatarSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user.avatar.delete(save=True)
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubscriptionsListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        author_ids = Subscription.objects.filter(user=user).values_list('author_id', flat=True)
        return User.objects.filter(id__in=author_ids)
