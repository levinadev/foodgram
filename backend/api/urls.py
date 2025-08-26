from django.urls import path
from .views import AvatarUpdateView

urlpatterns = [
    path("users/me/avatar/", AvatarUpdateView.as_view(), name="user-avatar"),
]
