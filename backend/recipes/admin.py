from django.contrib import admin
from django.db.models import Count

from .models import (
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredient,
    ShoppingCart,
    Tag,
)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("name", "author", "get_favorites_count")
    search_fields = ("name", "author__username", "author__email")
    list_filter = ("tags",)

    @admin.display(description="Количество в избранном")
    def get_favorites_count(self, obj):
        return obj.favorites.count()

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(favorite_count=Count("favorites"))


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name", "measurement_unit")
    search_fields = ("name",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name", "slug")


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ("recipe", "ingredient", "amount")
    search_fields = ("recipe__name", "ingredient__name")


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("user", "recipe")
    search_fields = ("user__email", "recipe__name")


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ("user", "recipe")
    search_fields = ("user__email", "recipe__name")
