import logging
from io import BytesIO

from django.db.models import Sum
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from api.filters import RecipeFilter
from recipes.models import (
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredient,
    ShoppingCart,
    Tag,
)
from users.models import Subscription, User

from .permissions import IsAuthorOrReadOnly
from .serializers import (
    AvatarSerializer,
    IngredientSerializer,
    RecipeCreateSerializer,
    RecipeSerializer,
    ShortRecipeSerializer,
    TagSerializer,
    UserCreateSerializer,
    UserSerializer,
)

logger = logging.getLogger(__name__)


class UserViewSet(DjoserUserViewSet):
    serializer_class = UserSerializer
    create_serializer_class = UserCreateSerializer

    @action(["get"], detail=False, permission_classes=[IsAuthenticated])
    def me(self, request, *args, **kwargs):
        """Профиль текущего пользователя."""
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(serializer.data)

    @action(["get"], detail=False, permission_classes=[IsAuthenticated])
    def subscriptions(self, request, *args, **kwargs):
        """Список подписок текущего пользователя."""
        author_ids = Subscription.objects.filter(
            user=request.user
        ).values_list("author_id", flat=True)
        queryset = User.objects.filter(id__in=author_ids)

        page = self.paginate_queryset(queryset)
        serializer = UserSerializer(
            page or queryset,
            many=True,
            context={"request": request, "include_recipes": True},
        )
        if page:
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)

    @action(
        ["post", "delete"], detail=True, permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, id=None, *args, **kwargs):
        """Подписка/отписка от пользователя."""
        author = get_object_or_404(User, pk=id)

        if request.method == "POST":
            if request.user == author:
                return Response(
                    {"errors": "Нельзя подписаться на самого себя"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if Subscription.objects.filter(
                user=request.user, author=author
            ).exists():
                return Response(
                    {"errors": "Вы уже подписаны на этого пользователя"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            Subscription.objects.create(user=request.user, author=author)
            serializer = UserSerializer(
                author, context={"request": request, "include_recipes": True}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        deleted, _ = Subscription.objects.filter(
            user=request.user, author=author
        ).delete()
        if not deleted:
            return Response(
                {"errors": "Вы не были подписаны"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        ["put", "delete"],
        detail=False,
        url_path="me/avatar",
        permission_classes=[IsAuthenticated],
    )
    def avatar(self, request, *args, **kwargs):
        """Загрузка/удаление аватара."""
        user = request.user

        if request.method == "PUT":
            if "avatar" not in request.data:
                return Response(
                    {"errors": "Поле avatar обязательно"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer = AvatarSerializer(
                user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        user.avatar.delete(save=True)
        return Response(status=status.HTTP_204_NO_CONTENT)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly,
    ]

    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return RecipeSerializer
        return RecipeCreateSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.is_authenticated:
            tags = self.request.query_params.getlist("tags")
            if tags:
                qs = qs.filter(tags__slug__in=tags).distinct()
            if self.request.query_params.get("is_favorited") == "1":
                qs = qs.filter(favorites__user=user)
        return qs

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=["get"], url_path="get-link")
    def get_link(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        relative_url = reverse("recipes-detail", kwargs={"pk": recipe.id})
        short_link = request.build_absolute_uri(relative_url)
        return Response({"short-link": short_link})

    def _add_to_relation(self, model, recipe):
        obj, created = model.objects.get_or_create(
            user=self.request.user, recipe=recipe
        )
        if not created:
            return None
        return obj

    def _remove_from_relation(self, model, recipe):
        deleted, _ = model.objects.filter(
            user=self.request.user, recipe=recipe
        ).delete()
        if not deleted:
            return None
        return True

    @action(detail=True, methods=["post", "delete"], url_path="favorite")
    def favorite(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == "POST":
            obj = self._add_to_relation(Favorite, recipe)
            if not obj:
                return Response(
                    {"errors": "Уже в избранном"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            return Response(
                ShortRecipeSerializer(recipe).data,
                status=status.HTTP_201_CREATED,
            )
        return (
            Response(status=status.HTTP_204_NO_CONTENT)
            if self._remove_from_relation(Favorite, recipe)
            else Response(
                {"errors": "Рецепт не был в избранном"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        )

    @action(detail=True, methods=["post", "delete"], url_path="shopping_cart")
    def shopping_cart(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == "POST":
            obj = self._add_to_relation(ShoppingCart, recipe)
            if not obj:
                return Response(
                    {"errors": "Уже в списке покупок"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            return Response(
                ShortRecipeSerializer(recipe).data,
                status=status.HTTP_201_CREATED,
            )
        return (
            Response(status=status.HTTP_204_NO_CONTENT)
            if self._remove_from_relation(ShoppingCart, recipe)
            else Response(
                {"errors": "Рецепта не было в списке покупок"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        )

    def _get_shopping_cart_ingredients(self, user):
        return (
            RecipeIngredient.objects.filter(recipe__shopping_carts__user=user)
            .values("ingredient__name", "ingredient__measurement_unit")
            .annotate(total_amount=Sum("amount"))
            .order_by("ingredient__name")
        )

    def _format_shopping_list(self, ingredients):
        return "\n".join(
            f"{ing['ingredient__name']} "
            f"({ing['ingredient__measurement_unit']}) — "
            f"{ing['total_amount']}"
            for ing in ingredients
        )

    @action(detail=False, methods=["get"], url_path="download_shopping_cart")
    def download_shopping_cart(self, request):
        ingredients = self._get_shopping_cart_ingredients(request.user)
        content = self._format_shopping_list(ingredients)

        file_like = BytesIO(content.encode("utf-8"))
        response = FileResponse(
            file_like,
            as_attachment=True,
            filename="shopping_list.txt",
            content_type="text/plain",
        )
        return response


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для ингредиентов."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [AllowAny]
    pagination_class = None

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get("name")
        if name:
            queryset = queryset.filter(name__istartswith=name)
        return queryset


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]
    pagination_class = None
