from django.contrib import admin
from django.contrib.auth.hashers import make_password
from .models import User, Subscription

@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not change or "password" in form.changed_data:
            obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)

admin.site.register(Subscription)
