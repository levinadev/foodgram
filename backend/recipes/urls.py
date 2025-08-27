# recipes/urls.py
from django.urls import path
from .views import RecipesStubView

urlpatterns = [
    path("", RecipesStubView.as_view(), name="recipes_stub"),
]
