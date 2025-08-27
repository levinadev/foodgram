from django.urls import path
from .views import (
    AvatarView,
    SubscriptionsListView
)

urlpatterns = [
    path("me/avatar/", AvatarView.as_view(), name="user-avatar"),
    path("subscriptions/", SubscriptionsListView.as_view(), name="user-subscriptions"),
]
