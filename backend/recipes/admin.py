from django.contrib import admin
from .models import Recipe, RecipeIngredient, Favorite

admin.site.register(Recipe)
admin.site.register(RecipeIngredient)
admin.site.register(Favorite)
