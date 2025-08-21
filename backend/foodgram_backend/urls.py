from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, re_path

urlpatterns = [
    path("admin/", admin.site.urls),
    re_path(r'^api/', include('djoser.urls')),
    re_path(r'^api/', include('djoser.urls.authtoken')),

    # алиас для фронта
    path("api/auth/", include("djoser.urls")),
    path("api/auth/", include("djoser.urls.authtoken")),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
