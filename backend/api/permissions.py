from rest_framework import permissions


class IsAuthorAndAuthenticatedOrReadOnly(permissions.BasePermission):
    """
    - Любой может читать.
    - Только авторизованный может создавать.
    - Изменять/удалять может только автор.
    """

    def has_permission(self, request, view):
        # безопасные методы доступны всем
        if request.method in permissions.SAFE_METHODS:
            return True
        # для create нужен просто авторизованный
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # безопасные методы доступны всем
        if request.method in permissions.SAFE_METHODS:
            return True
        # изменять/удалять только автору
        return obj.author == request.user
