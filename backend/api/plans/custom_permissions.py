import logging
from django.utils import timezone

from rest_framework import permissions

logger = logging.getLogger(__name__)


class CanChangeFuturePlans(permissions.BasePermission):
    """Права доступа для изменения будущих планов."""

    def has_object_permission(self, request, view, obj):
        if request.user.has_perm("plans.change_old_plan"):
            return True

        if obj.assigned_date < timezone.now().date():
            return False

        return True


class CanDeleteFuturePlans(permissions.BasePermission):
    """Права доступа для удаление будущих планов."""

    def has_object_permission(self, request, view, obj):
        if request.user.has_perm("plans.delete_old_plan"):
            return True

        if obj.assigned_date < timezone.now().date():
            return False

        return True
