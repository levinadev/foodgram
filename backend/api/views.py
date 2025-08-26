from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .serializers import AvatarSerializer


class AvatarUpdateView(generics.UpdateAPIView):
    serializer_class = AvatarSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user.avatar.delete(save=True)
        return Response(status=status.HTTP_204_NO_CONTENT)
