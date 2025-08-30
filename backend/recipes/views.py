from django.conf import settings
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.http import HttpResponse
from django.db.models import Sum

from .models import (
    Recipe,
    Favorite,
    RecipeIngredient,
    ShoppingCart
)

from .serializers import (
    RecipeSerializer,
    RecipeCreateSerializer,
    ShortRecipeSerializer
)
from .filters import RecipeFilter  # FIXME позже создадим фильтр

import logging

logger = logging.getLogger(__name__)


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

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user

        # Временная фильтрация по избранному (до фильтров через DjangoFilterBackend)
        if self.request.query_params.get("is_favorited") == "1" and user.is_authenticated:
            qs = qs.filter(favorites__user=user)

        return qs

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=["get"], url_path="get-link")
    def get_link(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        short_link = f"{settings.FRONTEND_URL}/recipes/{recipe.id}"
        return Response({"short-link": short_link})

    @action(detail=True, methods=["post", "delete"], url_path="favorite")
    def favorite(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)

        if request.method == "POST":
            obj, created = Favorite.objects.get_or_create(user=request.user, recipe=recipe)
            if not created:
                return Response(
                    {"errors": "Уже в избранном"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer = ShortRecipeSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == "DELETE":
            deleted, _ = Favorite.objects.filter(user=request.user, recipe=recipe).delete()
            if not deleted:
                return Response(
                    {"errors": "Рецепт не был в избранном"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["post", "delete"], url_path="shopping_cart")
    def shopping_cart(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)

        if request.method == "POST":
            obj, created = ShoppingCart.objects.get_or_create(
                user=request.user, recipe=recipe
            )
            if not created:
                return Response(
                    {"errors": "Уже в списке покупок"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer = ShortRecipeSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == "DELETE":
            deleted, _ = ShoppingCart.objects.filter(
                user=request.user, recipe=recipe
            ).delete()
            if not deleted:
                return Response(
                    {"errors": "Рецепта не было в списке покупок"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["get"], url_path="download_shopping_cart")
    def download_shopping_cart(self, request):
        ingredients = (
            RecipeIngredient.objects
            .filter(recipe__in_shopping_cart__user=request.user)
            .values("ingredient__name", "ingredient__measurement_unit")
            .annotate(total_amount=Sum("amount"))
            .order_by("ingredient__name")
        )

        shopping_list = []
        for ing in ingredients:
            shopping_list.append(
                f"{ing['ingredient__name']} ({ing['ingredient__measurement_unit']}) — {ing['total_amount']}"
            )

        # Формируем TXT-файл
        content = "\n".join(shopping_list)
        response = HttpResponse(content, content_type="text/plain")
        response["Content-Disposition"] = "attachment; filename=shopping_list.txt"
        return response
