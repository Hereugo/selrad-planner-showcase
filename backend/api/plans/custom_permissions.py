import logging
from django.utils import timezone

from functools import wraps
from rest_framework import permissions
from rest_framework.permissions import BasePermission
from rest_framework.response import Response


logger = logging.getLogger(__name__)


class CanChangeFuturePlans(permissions.BasePermission):
    """Права доступа для изменения будущих планов."""

    def has_object_permission(self, request, view, obj):
        if request.user.has_perm("plans.change_old_plan"):
            return True

        if obj.assigned_date < timezone.now().date():
            return False

        return True
