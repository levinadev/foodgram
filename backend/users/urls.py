from django.urls import path
from .views import (
    AvatarUpdateView,
    SubscriptionsListView
)

urlpatterns = [
    path("me/avatar/", AvatarUpdateView.as_view(), name="user-avatar"),
    path("subscriptions/", SubscriptionsListView.as_view(), name="user-subscriptions"),
]
