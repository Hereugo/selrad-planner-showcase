import logging

from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, UpdateModelMixin

from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status

from .serializers import (
    GeoPointCreateSerializer,
    GeoPointSerializer,
    ManagerSerializer,
    MeSerializer,
)

from api.utils.custom_permissions import IsAuthenticated, HasCRUDPermission, permission_required

from managers.models import Manager


User = get_user_model()
logger = logging.getLogger(__name__)


class UserViewSet(GenericViewSet, ListModelMixin, UpdateModelMixin):
    """API для работы с пользователями."""

    queryset = Manager.objects.filter(is_hidden=False)
    serializer_class = ManagerSerializer
    pagination_class = None
    permission_classes = (IsAuthenticated, HasCRUDPermission, )

    @extend_schema(
        methods=["get"],
        summary="Получение данных текущего пользователя.",
        parameters=[
            OpenApiParameter(
                name="geo_limit",
                type=int,
                required=False,
            )
        ],
        responses={200: MeSerializer},
    )
    @action(
        detail=False,
        methods=["get"],
        url_path="me",
        permission_classes=[IsAuthenticated],
    )
    def me(self, request):
        """Возвращает данные текущего пользователя."""
        if request.user.manager == None:
            return Response(
                {"error": "Пользователь не является менеджером"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = MeSerializer(request.user.manager)
        return Response(serializer.data)

    @extend_schema(
        methods=["get"],
        summary="Получить всех менеджеров",
        description="Получить всех менеджеров",
        parameters=[
            OpenApiParameter(
                name="geo_limit",
                type=int,
                required=False,
            )
        ],
    )
    @action(
        detail=False,
        methods=["get"],
        url_path="managers",
        permission_classes=[IsAuthenticated],
    )
    def managers(self, request):
        """Получить всех менеджеров."""
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(is_manager=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        methods=["get"],
        summary="Получить всех водителей",
        description="Получить всех водителей",
        parameters=[
            OpenApiParameter(
                name="geo_limit",
                type=int,
                required=False,
            )
        ],
    )
    @action(
        detail=False,
        methods=["get"],
        url_path="drivers",
        permission_classes=[IsAuthenticated],
    )
    def drivers(self, request):
        """Получить всех водителей."""
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(is_driver=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        methods=["get"],
        summary="Получить всех складовщиков",
        description="Получить всех складовщиков",
        parameters=[
            OpenApiParameter(
                name="geo_limit",
                type=int,
                required=False,
            )
        ],
    )
    @action(
        detail=False,
        methods=["get"],
        url_path="warehousers",
        permission_classes=[IsAuthenticated],
    )
    def warehousers(self, request):
        """Получить всех складовщиков."""
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(is_warehouser=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        request=GeoPointCreateSerializer,
        methods=["POST"],
        summary="Создание новой геоточки для текущего пользователя.",
        description='поле "manager" не передается в запросе, оно заполняется автоматически.',
        responses={201: GeoPointSerializer},
    )
    @action(
        detail=False,
        methods=["POST"],
        url_path="me/add_geopoint",
        permission_classes=[IsAuthenticated],
    )
    def add_geopoint(self, request):
        """Создание новой геоточки."""
        if request.user.manager == None:
            return Response(
                {"error": "Пользователь не является менеджером"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = GeoPointCreateSerializer(
            data=request.data, context={"request": request}
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )
