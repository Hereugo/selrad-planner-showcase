import json
import logging
from datetime import datetime
from io import BytesIO
from tempfile import TemporaryFile
from typing import Optional, cast

import pandas as pd
from django.db.models import QuerySet
from django.http import HttpResponse
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from html2image import Html2Image
from PIL import Image
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.v1.exports.custom_schemas import *
from api.v1.exports.serializers import DispatchListFilterSerializer
from api.v1.plans.serializers import PlanSerializer
from api.v1.plans.views import GenericPlanViewSet
from api.v1.utils.aws_lambda import get_lambda_client
from api.v1.utils.custom_permissions import IsAuthenticated, permission_required
from managers.models import Manager
from plans.models import Plan

logger = logging.getLogger(__name__)


class ExportDispatchList(GenericPlanViewSet, GenericViewSet):
    @extend_schema(
        parameters=[DispatchListFilterSerializer],
        responses=DEFAULT_FILE_RESPONSE,
        summary="Получить диспетчерский лист",
    )
    @action(
        detail=False,
        methods=["get"],
        permission_classes=[IsAuthenticated],
        url_path="aws_dispatch_list",
    )
    @permission_required("plans.get_dispatch_list")
    def aws_dispatch_list(self, request: Request) -> HttpResponse:
        filter_serializer = DispatchListFilterSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)

        start_date: Optional[datetime] = filter_serializer.validated_data["start_date"]
        end_date: Optional[datetime] = filter_serializer.validated_data["end_date"]
        comment: str = filter_serializer.validated_data["comment"]
        manager: Manager = filter_serializer.validated_data["manager"]

        plans: QuerySet[Plan] = self.filter_queryset(self.get_queryset())
        plans = plans.filter(managers=manager)
        plans = plans.order_by("assigned_date")
        if not start_date:
            start_date = cast(datetime, plans.earliest("assigned_date").assigned_date)
        if not end_date:
            end_date = cast(datetime, plans.latest("assigned_date").assigned_date)

        plans_serializer = PlanSerializer(plans, many=True)

        lambda_client = get_lambda_client()
        lambda_payload = {
            "start_date": start_date.strftime("%d.%m.%Y"),
            "end_date": end_date.strftime("%d.%m.%Y"),
            "comment": comment,
            "manager_name": manager.name,
            "plans": plans_serializer.data,
        }
        response = lambda_client.invoke(
            FunctionName="export-dispatch-list",
            InvocationType="RequestResponse",
            Payload=json.dumps(lambda_payload),
        )
        response = json.loads(response["Payload"].read().decode("utf-8"))

        return Response(response)

    @extend_schema(
        parameters=[DispatchListFilterSerializer],
        responses=DEFAULT_FILE_RESPONSE,
        summary="Получить диспетчерский лист",
    )
    @action(
        detail=False,
        methods=["get"],
        permission_classes=[IsAuthenticated],
        url_path="dispatch_list",
    )
    @permission_required("plans.get_dispatch_list")
    def dispatch_list(self, request: Request) -> HttpResponse:
        filter_serializer = DispatchListFilterSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)

        start_date: Optional[datetime] = filter_serializer.validated_data["start_date"]
        end_date: Optional[datetime] = filter_serializer.validated_data["end_date"]
        comment: str = filter_serializer.validated_data["comment"]
        manager: Manager = filter_serializer.validated_data["manager"]

        plans: QuerySet[Plan] = self.filter_queryset(self.get_queryset())
        plans = plans.filter(managers=manager)
        plans = plans.order_by("assigned_date")

        if filter_serializer.validated_data["set_time_dispatch"]:
            plans.filter(time_since_first_dispatch__isnull=True).update(
                time_since_first_dispatch=timezone.now()
            )

        if not start_date:
            start_date = cast(datetime, plans.earliest("assigned_date").assigned_date)
        if not end_date:
            end_date = cast(datetime, plans.latest("assigned_date").assigned_date)

        buffer = generate_dispatch_list(plans, manager, comment, start_date, end_date)
        buffer.seek(0)

        # response = FileResponse(
        #     buffer,
        #     as_attachment=True,
        #     filename=f"ДИСПЕТЧЕРСКИЙ ЛИСТ {manager.name} С {start_date.strftime('%d-%m-%Y')} ПО {end_date.strftime('%d-%m-%Y')}.png",
        #     content_type="image/png",
        # )

        response = HttpResponse(
            buffer.getvalue(),
            content_type="image/png",
        )
        response["Access-Control-Expose-Headers"] = "Content-Disposition"
        response["Content-Disposition"] = (
            f"attachment; filename=\"ДИСПЕТЧЕРСКИЙ ЛИСТ {manager.name} С {start_date.strftime('%d-%m-%Y')} ПО {end_date.strftime('%d-%m-%Y')}.png\""
        )

        buffer.close()

        return response


def generate_dispatch_list(
    plans: QuerySet[Plan],
    manager: Manager,
    comment: str,
    start_date: datetime,
    end_date: datetime,
):
    l = {
        "№\nп/п": [],
        "Клиент": [],
        "Кол-во коробок": [],
        "Место Отгрузки": [],
        "Контактное лицо": [],
        "Доп информация": [],
        "Доп информация бух": [],
    }
    for i, plan in enumerate(plans, start=1):
        l["№\nп/п"].append(i)
        l["Клиент"].append(plan.client.name)
        l["Кол-во коробок"].append(plan.box_count)
        l["Место Отгрузки"].append(plan.client.address.street)
        l["Контактное лицо"].append(", ".join([m.name for m in plan.managers.all()]))
        l["Доп информация"].append(plan.comment)
        l["Доп информация бух"].append(plan.accountant_comment)

    df = pd.DataFrame(l)

    buffer = BytesIO()
    hti = Html2Image(
        browser_executable="google-chrome",
        custom_flags=["--no-sandbox", "--hide-scrollbars", "--quiet"],
        output_path="./static/temp/",
    )
    with TemporaryFile(mode="w+") as f:
        df.to_html(f, index=False)
        f.seek(0)

        html_str = f"""
        <h1>Диспечерский лист {manager.name}</h1>
        <span>Параметры:</span><br />
        <span>Период: {start_date.strftime("%d.%m.%Y")} с {end_date.strftime("%d.%m.%Y")}</span><br />
        <span>Менеджер: {manager.name}</span><br />
        <br />
        {f.read()}
        <h1 style="margin-left: calc(674px - 8ch);">ИТОГО: {sum(x.box_count for x in plans)}</h1>
        <br />
        <h1>{comment}</h1>
        """

        css_str = "table,th,tr,td{border:1px solid #000;background-color:white;}*{box-sizing:border-box;font-family:Arial,sans-serif;background-color:white;}table{border-collapse:collapse;width:100%}th{background-color:#d3d3d3;font-size:14px;font-weight:700;text-align:left}td,th{padding:8px}tr th:first-child{width:24px;max-width:24px}tr th:nth-child(2),tr th:nth-child(4){width:300px;max-width:300px}tr th:nth-child(3){width:50px;max-width:50px}tr td:nth-child(3){font-size:20px;font-weight:700;text-align:center}tr th:nth-child(5){width:200px;max-width:200px}tr th:nth-child(6){width:100px;max-width:100px}tr th:nth-child(7){width:100px;max-width:100px}"

        calc_height = 500 + len(df) * 55

        img = hti.screenshot(
            html_str,
            css_str=css_str,
            save_as="html_table.png",
            size=(1920, calc_height),
        )

        logger.debug(img)

        image = Image.open(img[0])

        # rotate image clockwise 90
        rotated_image = image.rotate(-90, expand=1)

        rotated_image.save(buffer, format="png", optimize=True, quality=95)
        buffer.seek(0)

        image.close()

    # delete html_table

    return buffer
