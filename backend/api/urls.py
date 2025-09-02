from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import (
    IngredientViewSet, TagViewSet, RecipeViewSet,
    AvatarView, SubscriptionsView
)

router = DefaultRouter()
router.register(r"recipes", RecipeViewSet, basename="recipes")
router.register(r"ingredients", IngredientViewSet, basename="ingredients")
router.register(r"tags", TagViewSet, basename="tags")

urlpatterns = router.urls


urlpatterns += [
    path(
        "users/me/avatar/",
        AvatarView.as_view(),
        name="user-avatar"
    ),
    path(
        "users/subscriptions/",
        SubscriptionsView.as_view(),
        name="user-all-subscriptions"
    ),
    path(
        "users/<int:id>/subscribe/",
        SubscriptionsView.as_view(),
        name="user-subscription-unsubscribe"
    ),
]
