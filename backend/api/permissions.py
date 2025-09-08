from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Разрешение для работы с объектами:

    - Чтение доступно всем пользователям.
    - Изменение и удаление разрешено только автору объекта.
    """

    def has_object_permission(self, request, view, obj):
        """Проверка прав на уровне объекта."""
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )
