from rest_framework import permissions

from reviews.models import ADMIN, MODERATOR


class IsAuthorOrStaffOrReadOnly(permissions.BasePermission):
    """Доступ на чтение для всех. На запись только для автора,
    администратора,модератора или суперюзера."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user == obj.author
            or request.user.role == ADMIN
            or request.user.role == MODERATOR
            or request.user.is_superuser
        )


class IsAdmin(permissions.BasePermission):
    """Доступ только администратору или суперюзеру."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.role == ADMIN
            or request.user.is_superuser
        )


class AdminOrReadOnly(permissions.BasePermission):
    """Доступ на чтение для всех. На запись только
    для администратора или суперюзера."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and (request.user.role == ADMIN
                 or request.user.is_superuser)
        )
