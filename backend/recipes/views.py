from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .models import Recipe
from .serializers import RecipeSerializer
from .filters import RecipeFilter  # FIXME позже создадим фильтр


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # filter_backends = [DjangoFilterBackend] # FIXME позже создадим фильтр
    # filterset_class = RecipeFilter # FIXME позже создадим фильтр

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
