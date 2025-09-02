from django.contrib import admin
from django.db.models import Count

from .models import (
    Favorite, Recipe,
    RecipeIngredient, ShoppingCart,
    Tag, Ingredient
)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ("name", "author", "get_favorites_count")
    search_fields = ("name", "author__username", "author__email")
    list_filter = ("tags",)

    def get_favorites_count(self, obj):
        return obj.favorites.count()

    get_favorites_count.short_description = "Favorite Count"

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(favorite_count=Count("favorites"))


class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name", "measurement_unit")

    search_fields = ("name",)


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient)
admin.site.register(Favorite)
admin.site.register(ShoppingCart)
