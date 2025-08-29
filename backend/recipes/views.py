from rest_framework import viewsets, permissions
from .models import Recipe

from .serializers import RecipeSerializer, RecipeCreateSerializer
from .filters import RecipeFilter  # FIXME позже создадим фильтр


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # filter_backends = [DjangoFilterBackend] # FIXME позже создадим фильтр
    # filterset_class = RecipeFilter # FIXME позже создадим фильтр

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return RecipeCreateSerializer
        return RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
