from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AvatarView,
    IngredientViewSet,
    MeView,
    RecipeViewSet,
    SubscriptionsView,
    TagViewSet,
)

router = DefaultRouter()
router.register(r"recipes", RecipeViewSet, basename="recipes")
router.register(r"ingredients", IngredientViewSet, basename="ingredients")
router.register(r"tags", TagViewSet, basename="tags")


urlpatterns = [
    path("auth/", include("djoser.urls.authtoken")),
    path("", include(router.urls)),
    path(
        "users/subscriptions/",
        SubscriptionsView.as_view(),
        name="user-all-subscriptions",
    ),
    path("users/me/", MeView.as_view(), name="user-me"),
    path("", include("djoser.urls")),
    path("users/me/avatar/", AvatarView.as_view(), name="user-avatar"),
    path(
        "users/<int:id>/subscribe/",
        SubscriptionsView.as_view(),
        name="user-subscription-unsubscribe",
    ),
]
