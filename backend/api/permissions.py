from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Только автор может изменять/удалять объект.
    Остальным доступен только просмотр.
    """

    def has_object_permission(self, request, view, obj):
        # безопасные методы (GET, HEAD, OPTIONS) разрешены всем
        if request.method in permissions.SAFE_METHODS:
            return True
        # изменение/удаление только для автора
        return obj.author == request.user
