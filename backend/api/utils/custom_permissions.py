import logging

from functools import wraps
from rest_framework import permissions
from rest_framework.permissions import BasePermission
from rest_framework.response import Response


logger = logging.getLogger(__name__)


class IsReadOnly(permissions.BasePermission):
    """Права доступа только для чтения."""

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsAuthenticated(permissions.BasePermission):
    """Права доступа только для авторизованных."""

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """
    Права доступа для чтения всем, а для записи только для авторизованных.
    """

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        return False


class HasCRUDPermission(BasePermission):
    """Права доступа для сотрудников."""

    def has_permission(self, request, view):
        app_label = view.queryset.model._meta.app_label
        model_name = view.queryset.model._meta.model_name

        if request.method == "GET":
            return request.user.has_perm(f"{app_label}.view_{model_name}")
        if request.method == "POST":
            return request.user.has_perm(f"{app_label}.add_{model_name}")
        if request.method in ("PUT", "PATCH"):
            return request.user.has_perm(f"{app_label}.change_{model_name}")
        if request.method == "DELETE":
            return request.user.has_perm(f"{app_label}.delete_{model_name}")
        return False


def permission_required(permission):
    def has_permission_decorator(func):
        @wraps(func)
        def has_permission_wrapper(*args, **kwargs):
            request = args[0].request
            if not request.user.has_perm(permission):
                return Response(
                    {"error": "У вас нет прав на это действие."}, status=403
                )
            return func(*args, **kwargs)

        return has_permission_wrapper

    return has_permission_decorator
