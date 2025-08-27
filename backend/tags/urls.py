# recipes/urls.py
from django.urls import path
from .views import TagsStubView

urlpatterns = [
    path("", TagsStubView.as_view(), name="tags_stub"),
]
