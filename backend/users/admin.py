from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.hashers import make_password

from .models import Subscription, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_active",
        "recipes_count",
        "subscribers_count",
    )
    search_fields = ("username", "email")
    list_filter = ("is_active", "is_staff", "is_superuser")

    @admin.display(description="Рецептов")
    def recipes_count(self, obj):
        return obj.recipes.count()

    @admin.display(description="Подписчиков")
    def subscribers_count(self, obj):
        return obj.subscribers.count()

    def save_model(self, request, obj, form, change):
        if not change or "password" in form.changed_data:
            obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("user", "author")
    search_fields = ("user__email", "author__email")
