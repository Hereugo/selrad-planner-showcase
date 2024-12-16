import logging
from django.utils import timezone

from rest_framework import permissions

logger = logging.getLogger(__name__)


# COMMENTED:
# Object level permissions are done in serializer instead of in view.
#
# Only read, update, and destroy are object level permissions. So
# create permission wont activate CanAddFuturePlans.
# Therefore I've moved permission for update to serializer.
# https://www.django-rest-framework.org/api-guide/permissions/
#
# class CanAddFuturePlans(permissions.BasePermission):
#     """Права доступа для изменения будущих планов."""
#
#     def has_object_permission(self, request, view, obj):
#         if request.user.has_perm("plans.add_old_plan"):
#             return True
#
#         if obj.assigned_date < timezone.now().date():
#             return False
#
#         return True
#
#
# class CanChangeFuturePlans(permissions.BasePermission):
#     """Права доступа для изменения будущих планов."""
#
#     def has_object_permission(self, request, view, obj):
#         if request.user.has_perm("plans.change_old_plan"):
#             return True
#
#         if obj.assigned_date < timezone.now().date():
#             return False
#
#         return True


class CanDeleteFuturePlans(permissions.BasePermission):
    """Права доступа для удаление будущих планов."""

    def has_object_permission(self, request, view, obj):
        if request.user.has_perm("plans.delete_old_plan"):
            return True

        if obj.assigned_date < timezone.now().date():
            return False

        return True