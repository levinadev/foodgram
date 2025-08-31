from django.urls import path

from .views import AvatarView, SubscriptionsView

urlpatterns = [
    path("me/avatar/", AvatarView.as_view(), name="user-avatar"),
    path("subscriptions/", SubscriptionsView.as_view(), name="user-all-subscriptions"),
    path("<int:id>/subscribe/", SubscriptionsView.as_view(), name="user-subscription-unsubscribe"),
]
