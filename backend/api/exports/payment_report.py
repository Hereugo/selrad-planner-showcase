import logging
from datetime import datetime
from io import BytesIO
from typing import Any, Optional, cast

import openpyxl
import pandas as pd
from api.plans.views import GenericPlanViewSet
from api.utils.custom_permissions import IsAuthenticated, permission_required
from django.db import models
from django.db.models import F, OuterRef, Subquery
from django.http import FileResponse
from openpyxl.utils import get_column_letter
from openpyxl.utils.dataframe import dataframe_to_rows
from plans.models import PaymentRegistry
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.viewsets import GenericViewSet

from .custom_schemas import *
from .serializers import PaymentReportFilterSerializer

logger = logging.getLogger(__name__)


class ExportPaymentReport(GenericPlanViewSet, GenericViewSet):

    @extend_schema(
        summary="Скачать отчет по выплатам",
        parameters=[PaymentReportFilterSerializer],
        responses=DEFAULT_FILE_RESPONSE,
    )
    @action(
        detail=False,
        methods=["get"],
        permission_classes=[IsAuthenticated],
        url_path="payment_report",
    )
    @permission_required("plans.export_payment_report")
    def payment_report(self, request: Request) -> FileResponse:
        filter_serializer = PaymentReportFilterSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)

        start_date: Optional[datetime] = filter_serializer.validated_data["start_date"]
        end_date: Optional[datetime] = filter_serializer.validated_data["end_date"]

        plans = self.filter_queryset(self.get_queryset())

        if not start_date:
            start_date = cast(datetime, plans.earliest("assigned_date").assigned_date)
        if not end_date:
            end_date = cast(datetime, plans.latest("assigned_date").assigned_date)

        # Subquery to fetch total payments for each manager and assigned_date
        payments_subquery = (
            PaymentRegistry.objects.filter(
                date=OuterRef("assigned_date"),
                manager__id=OuterRef("managers__id"),
                is_confirmed=True,  # Go only through confirmed payments
            )
            .annotate(payment_bonus=F("payment") + F("bonus"))
            .values("payment_bonus")
        )

        # Query the plans and annotate with manager and payment data
        plans = (
            plans.prefetch_related("managers")
            .values(
                "pk",
                "assigned_date",
                "client__meta_client__name",
                "client__name",
                "box_count",
                "managers__id",
                "managers__name",
            )
            .annotate(
                payment_bonus=Subquery(
                    payments_subquery,
                    output_field=models.IntegerField(),
                ),
            )
            .annotate(
                manager_id=F("managers__id"),
                manager=F("managers__name"),
                shop=F("client__name"),
                client=F("client__meta_client__name"),
                date=F("assigned_date"),
            )
            .values(
                "manager",
                "shop",
                "client",
                "date",
                "box_count",
                "payment_bonus",
            )
        )

        buffer = generate_payment_report(list(plans))
        buffer.seek(0)

        response = FileResponse(
            buffer,
            as_attachment=True,
            filename=f"ОТЧЕТ ПО ВЫПЛАТАМ С {start_date.strftime('%d-%m-%Y')} ПО {end_date.strftime('%d-%m-%Y')}.png",
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

        return response


def generate_payment_report(table: list[dict[str, Any]]) -> BytesIO:
    workbook = openpyxl.Workbook()

    df = pd.DataFrame(table)

    # logger.debug(df.columns)
    # for c in df.columns:
    #     logger.debug(f"{c}: {df.columns.get_loc(c)} : {type(df.columns.get_loc(c))}")

    # get_column_letter starts from 1, so +1 is needed as first column index is 0.
    cols_by_letter = {
        c: get_column_letter(df.columns.get_loc(c) + 1) for c in df.columns
    }

    logger.debug(cols_by_letter).

    total_visit_count = "SUMPRODUCT(({shop}:{shop}={shop}1)*({manager}:{manager}={manager}1))".format_map(
        cols_by_letter
    )
    total_box_count = "SUMIFS({box_count}:{box_count}, {shop}:{shop}, {shop}1, {manager}:{manager}, {manager}1)".format_map(
        cols_by_letter
    )
    total_payment_bonus = "SUMIFS({payment_bonus}:{payment_bonus}, {shop}:{shop}, {shop}1, {manager}:{manager}, {manager}1)".format_map(
        cols_by_letter
    )

    df["total_visit_count"] = "=" + total_visit_count
    df["total_box_count"] = "=" + total_box_count
    df["total_payment_bonus"] = "=" + total_payment_bonus
    df["box_cost"] = "=" + total_payment_bonus + "/" + total_box_count

    raw_data_ws = workbook.create_sheet("raw_data")
    for r in dataframe_to_rows(df, index=False, header=True):
        raw_data_ws.append(r)

    buffer = BytesIO()
    workbook.save(buffer)

    return buffer
