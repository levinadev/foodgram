from rest_framework import permissions


class IsAuthorAndAuthenticatedOrReadOnly(permissions.BasePermission):
    """
    Разрешение для работы с объектами:

    - Чтение доступно всем пользователям.
    - Создание доступно только авторизованным пользователям.
    - Изменение и удаление разрешено только автору объекта.
    """

    def has_permission(self, request, view):
        """
        Проверяет доступ к действию на уровне запроса.

        - Безопасные методы (GET, HEAD, OPTIONS) доступны всем.
        - Для создания (POST) требуется авторизация.
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Проверяет доступ на уровне конкретного объекта.

        - Безопасные методы (GET, HEAD, OPTIONS) доступны всем.
        - Изменение и удаление разрешено только автору объекта.
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
