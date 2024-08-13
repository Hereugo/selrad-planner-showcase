import logging

from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from drf_spectacular.utils import extend_schema
from rest_framework import status

from api.managers.serializers import GeoPointCreateSerializer, GeoPointSerializer

from api.utils.custom_permissions import IsAuthenticated

from .serializers import UserSerializer


User = get_user_model()
logger = logging.getLogger(__name__)


class UserViewSet(mixins.ListModelMixin, GenericViewSet):
    """API для работы с пользователями."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = None
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        methods=["get"],
        summary="Получение данных текущего пользователя.",
    )
    @action(
        detail=False,
        methods=["get"],
        url_path="me",
        permission_classes=[IsAuthenticated],
    )
    def me(self, request):
        """Возвращает данные текущего пользователя."""
        serializer = self.get_serializer(request.user)
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
        if request.user.manager is None:
            raise Exception("User is not a manager")

        request.data["manager"] = request.user.manager.id
        serializer = GeoPointCreateSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )
