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


def get_cols_by_letter(df):
    return {
        c: get_column_letter(cast(int, df.columns.get_loc(c)) + 1) for c in df.columns
    }


def generate_payment_report(table: list[dict[str, Any]]) -> BytesIO:
    workbook = openpyxl.Workbook()

    df = pd.DataFrame(table)

    total_visit_count = "SUMPRODUCT(({sheet}!{shop}:{shop}=INDEX({sheet}!{shop}:{shop}, {row}))*({sheet}!{manager}:{manager}=INDEX({sheet}!{manager}:{manager},{row})))"
    total_box_count = "SUMIFS({sheet}!{box_count}:{box_count}, {sheet}!{shop}:{shop}, INDEX({sheet}!{shop}:{shop}, {row}), {sheet}!{manager}:{manager}, INDEX({sheet}!{manager}:{manager}, {row}))"
    total_payment_bonus = "SUMIFS({sheet}!{payment_bonus}:{payment_bonus}, {sheet}!{shop}:{shop}, INDEX({sheet}!{shop}:{shop}, {row}), {sheet}!{manager}:{manager}, INDEX({sheet}!{manager}:{manager}, {row}))"

    cols_by_letter = get_cols_by_letter(df)

    # Important to do it after cols_by_letter function, as it
    # errors when formatting of formulas are done.
    df["row"] = range(1, len(df) + 1)

    raw_data_ws = workbook.create_sheet("raw_data")
    for r in dataframe_to_rows(df, index=False, header=True):
        raw_data_ws.append(r)

    for manager, manager_group in df.groupby(by="manager"):
        manager = cast(str, manager)
        manager_ws = workbook.create_sheet(manager)
        # https://stackoverflow.com/questions/27133731/folding-multiple-rows-with-openpyxl
        manager_ws.sheet_properties.outlinePr.summaryBelow = False

        header = ["Клиент", "Коробки", "Кол-во выходов", "Выплаты", "Стоимость кор-ки"]
        manager_ws.append(header)

        group_rows_start = 2
        for client, client_manager_group in manager_group.groupby(by="client"):
            # Sub-header, that contains aggregated data.
            client_manager_rows = client_manager_group["row"]
            client_body_df = pd.DataFrame(
                {
                    "shop": client_manager_group["shop"],
                    "total_box_count": client_manager_rows.apply(
                        lambda x: "="
                        + total_box_count.format(
                            **cols_by_letter, sheet="raw_data", row=x + 1
                        )
                    ),
                    "total_visit_count": client_manager_rows.apply(
                        lambda x: "="
                        + total_visit_count.format(
                            **cols_by_letter, sheet="raw_data", row=x + 1
                        )
                    ),
                    "total_payment_count": client_manager_rows.apply(
                        lambda x: "="
                        + total_payment_bonus.format(
                            **cols_by_letter, sheet="raw_data", row=x + 1
                        )
                    ),
                    "box_cost": client_manager_rows.apply(
                        lambda x: "="
                        + total_payment_bonus.format(
                            **cols_by_letter, sheet="raw_data", row=x + 1
                        )
                        + "/"
                        + total_box_count.format(
                            **cols_by_letter, sheet="raw_data", row=x + 1
                        )
                    ),
                }
            )
            body_size = len(client_body_df)
            body_range = (group_rows_start + 1, group_rows_start + body_size)
            client_header_df = pd.DataFrame(
                {
                    "shop": [client],
                    "total_box_count": ["=SUM(B{}:B{})".format(*body_range)],
                    "total_visit_count": ["=SUM(C{}:C{})".format(*body_range)],
                    "total_payment_count": ["=SUM(D{}:D{})".format(*body_range)],
                    "box_cost": ["=D{0}/B{0}".format(group_rows_start)],
                }
            )

            client_table_df = pd.concat([client_header_df, client_body_df])

            for r in dataframe_to_rows(client_table_df, index=False, header=False):
                manager_ws.append(r)

            manager_ws.row_dimensions.group(
                group_rows_start + 1,
                group_rows_start + len(client_body_df),
                hidden=True,
                outline_level=1,
            )

            # move to next sub-header row
            group_rows_start += len(client_table_df)

        footer_range = (2, group_rows_start - 1)
        footer = [
            "Итого",
            "=SUM(B{}:B{})/2".format(*footer_range),
            "=SUM(C{}:C{})/2".format(*footer_range),
            "=SUM(D{}:D{})/2".format(*footer_range),
            "=C{0}/D{0}".format(group_rows_start),
        ]
        manager_ws.append(footer)

    buffer = BytesIO()
    workbook.save(buffer)

    return buffer
