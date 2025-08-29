from django.conf import settings
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

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

    @action(detail=True, methods=["get"], url_path="get-link")
    def get_link(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        short_link = f"{settings.FRONTEND_URL}/recipes/{recipe.id}"
        return Response({"short-link": short_link})
