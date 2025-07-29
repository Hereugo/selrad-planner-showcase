import logging
from datetime import datetime
from io import BytesIO
from typing import Any, List, Optional, cast

import openpyxl
import pandas as pd
from django.db.models import F, Prefetch, Q, Sum, Value
from django.db.models.functions import Coalesce, Concat
from django.http import HttpResponse
from drf_spectacular.utils import extend_schema
from openpyxl.styles import Border, Font, NamedStyle, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.utils.dataframe import dataframe_to_rows
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.viewsets import GenericViewSet

from api.v1.exports.custom_schemas import *
from api.v1.exports.serializers import DistributionCostReportFilterSerializer
from api.v1.plans.views import GenericPlanViewSet
from api.v1.utils.custom_permissions import IsAuthenticated, permission_required
from clients.models import Client
from managers.models import Manager

logger = logging.getLogger(__name__)


class ExportDistributionCostReport(GenericPlanViewSet, GenericViewSet):

    @extend_schema(
        summary="Скачать отчет по стоимоти дистрибуции",
        parameters=[DistributionCostReportFilterSerializer],
        responses=DEFAULT_FILE_RESPONSE,
    )
    @action(
        detail=False,
        methods=["get"],
        permission_classes=[IsAuthenticated],
        url_path="payment_report",
    )
    @permission_required("plans.export_distribution_cost_report")
    def distribution_cost_report(self, request: Request) -> HttpResponse:
        filter_serializer = DistributionCostReportFilterSerializer(
            data=request.query_params
        )
        filter_serializer.is_valid(raise_exception=True)

        start_date: Optional[datetime] = filter_serializer.validated_data["start_date"]
        end_date: Optional[datetime] = filter_serializer.validated_data["end_date"]
        managers: List[Manager] = filter_serializer.validated_data.get("managers", [])

        managers_qs = Manager.objects.filter(pk__in=[m.pk for m in managers])

        plans = self.filter_queryset(self.get_queryset())

        if not start_date:
            start_date = cast(datetime, plans.earliest("assigned_date").assigned_date)
        if not end_date:
            end_date = cast(datetime, plans.latest("assigned_date").assigned_date)
        if not managers:
            managers_qs = Manager.objects.all()
            managers = list(Manager.objects.all())

        plans = (
            plans.prefetch_related(
                Prefetch(
                    "manager_set",
                    queryset=managers_qs.prefetch_related("payment_registries"),
                )
            )
            .values(
                "assigned_date",
                "managers",
                "box_count",
                "shipment_cost_formula",
                "client__name",
                "client__meta_client__name",
            )
            .filter(
                Q(managers__in=managers)
                & Q(managers__payment_registries__is_confirmed=True)
                & Q(managers__payment_registries__date=F("assigned_date"))
            )
            .annotate(
                payment_bonus=Coalesce(
                    Sum(
                        F("managers__payment_registries__payment")
                        + F("managers__payment_registries__bonus")
                    ),
                    Value(0),
                ),
                manager=F("managers__name"),
                manager_id=F("managers__id"),
                is_driver=F("managers__is_driver"),
                shop=F("client__name"),
                client=F("client__meta_client__name"),
                date=F("assigned_date"),
                shipment_cost_formula=Concat(Value("="), F("shipment_cost_formula")),
            )
            .values(
                "payment_bonus",
                "manager",
                "manager_id",
                "is_driver",
                "shop",
                "client",
                "date",
                "box_count",
                "shipment_cost_formula",
            )
            .distinct()
        )

        buffer = generate_distribution_cost_report(list(plans))
        buffer.seek(0)

        response = HttpResponse(
            buffer.getvalue(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Access-Control-Expose-Headers"] = "Content-Disposition"
        response["Content-Disposition"] = (
            f"attachment; filename=\"ОТЧЕТ ПО СТОИМОТИ ДИСТРИБУЦИИ {', '.join([m.name for m in managers_qs]) if 'manager' in filter_serializer.validated_data else ''} С {start_date.strftime('%d-%m-%Y')} ПО {end_date.strftime('%d-%m-%Y')}.xlsx\""
        )

        buffer.close()

        return response


def get_cols_by_letter(df):
    return {
        c: get_column_letter(cast(int, df.columns.get_loc(c)) + 1) for c in df.columns
    }


def generate_distribution_cost_report(table: list[dict[str, Any]]) -> BytesIO:
    workbook = openpyxl.Workbook()

    # add raw table in separate spreadsheet
    total_box_count = "SUM(MAP(UNIQUE(FILTER({sheet}!{date}:{date}, {sheet}!{shop}:{shop}={sheet}!{shop}{row})), LAMBDA(h, XLOOKUP(h, FILTER({sheet}!{date}:{date}, {sheet}!{shop}:{shop}={sheet}!{shop}{row}), FILTER({sheet}!{box_count}:{box_count}, {sheet}!{date}:{date}={sheet}!{shop}{row})))))"
    total_shipment_cost = "SUM(MAP(UNIQUE(FILTER({sheet}!{date}:{date}, {sheet}!{shop}:{shop}={sheet}!{shop}{row})), LAMBDA(h, XLOOKUP(h, FILTER({sheet}!{date}:{date}, {sheet}!{shop}:{shop}={sheet}!{shop}{row}), FILTER({sheet}!{shipment_cost_formula}:{shipment_cost_formula}, {sheet}!{date}:{date}={sheet}!{shop}{row})))))"

    total_payment_bonus = {
        "driver": "SUMIFS({sheet}!{box_price}:{box_price}, {sheet}!{shop}:{shop}, INDEX({sheet}!{shop}:{shop}, {row}), {sheet}!{manager}:{manager}, INDEX({sheet}!{manager}:{manager}, {row}))",
        "manager": "SUMIFS({sheet}!{visit_price}:{visit_price}, {sheet}!{shop}:{shop}, INDEX({sheet}!{shop}:{shop}, {row}), {sheet}!{manager}:{manager}, INDEX({sheet}!{manager}:{manager}, {row}))",
    }

    box_price = "INDEX({sheet}!{payment_bonus}:{payment_bonus}, {row}) * INDEX({sheet}!{box_count}:{box_count}, {row}) / SUMIFS({sheet}!{box_count}:{box_count}, {sheet}!{date}:{date}, INDEX({sheet}!{date}:{date}, {row}), {sheet}!{manager}:{manager}, INDEX({sheet}!{manager}:{manager}, {row}))"
    visit_price = "INDEX({sheet}!{payment_bonus}:{payment_bonus}, {row}) / SUMPRODUCT(({sheet}!{date}:{date}=INDEX({sheet}!{date}:{date}, {row}))*({sheet}!{manager}:{manager}=INDEX({sheet}!{manager}:{manager},{row})))"

    df = pd.DataFrame(table)
    df["box_price"] = "=" + box_price.format(
        **get_cols_by_letter(df), sheet="raw_data", row="ROW()"
    )
    df["visit_price"] = "=" + visit_price.format(
        **get_cols_by_letter(df), sheet="raw_data", row="ROW()"
    )

    cols_by_letter = get_cols_by_letter(df)

    # Important to do it after cols_by_letter function, as it
    # errors when formatting of formulas are done.
    df["row"] = range(1, len(df) + 1)

    raw_data_ws = workbook.create_sheet("raw_data")
    raw_data_ws.title = "raw_data"
    for r in dataframe_to_rows(df, index=False, header=True):
        raw_data_ws.append(r)

    # create and fillout main worksheet
    ws = workbook.create_sheet()

    ws.cell(row=1, column=2).value = "Кол-во коробок (кор)"
    ws.cell(row=1, column=3).value = "Сумма отгрузки (₸)"
    ws.cell(row=3, column=1).value = "магазины / клиенты"

    group_rows_start = 0
    for client, shop_group in df.groupby(by="client"):
        # TABLE 1 CREATION
        table1_df = pd.DataFrame(
            {
                "shop": shop_group["shop"],
                "total_box_count": shop_group["row"].apply(
                    lambda x: "="
                    + total_box_count.format(
                        **cols_by_letter, sheet="raw_data", row=x + 1
                    )
                ),
                "total_shipment_cost": shop_group["row"].apply(
                    lambda x: "="
                    + total_shipment_cost.format(
                        **cols_by_letter, sheet="raw_data", row=x + 1
                    )
                ),
            }
        )
        table1_size = len(table1_df)
        table1_range = (group_rows_start + 1, group_rows_start + table1_size)
        table1_header_df = pd.DataFrame(
            {
                "shop": [client],
                "total_box_count": [
                    "=SUM({box_count_col}{}:{box_count_col}{}".format(
                        *table1_range,
                        box_count_col="B",
                    )
                ],
                "total_shipment_cost": [
                    "=SUM({shipment_cost_col}{}:{shipment_cost_col}{}".format(
                        *table1_range,
                        shipment_cost_col="C",
                    )
                ],
            }
        )

        for r in dataframe_to_rows(table1_header_df, index=False, header=False):
            ws.append(r)
            for cell in list(ws)[-1]:
                cell.style = "subgroup_header_cell"

        for r in dataframe_to_rows(table1_df, index=False, header=False):
            ws.append(r)
            for cell in list(ws)[-1]:
                cell.style = "generic_cell"

        # TABLE 2 CREATION (DRIVERS WITH PAYMENTS)

        table2_df = pd.DataFrame(
            {
                manager: client_manager_group["row"].apply(
                    lambda x: "=ROUND({}, 0)".format(
                        total_payment_bonus["driver"].format(
                            **cols_by_letter,
                            sheet="raw_data",
                            row=x + 1,
                        )
                    )
                )
                for manager, client_manager_group in shop_group.groupby(by="manager")
                if df.at(
                    client_manager_group["row"][0] - 1, "is_driver"
                )  # I'm not sure but it could be empty
            }
        )

        table2_offset = 4  # absolute offset from spreadsheet
        table2_size = len(table2_df)
        table2_range = (group_rows_start + 1, group_rows_start + table2_size)
        table2_header_df = pd.DataFrame(
            {
                manager: "=SUM({payment_bonus_col}{}:{payment_bonus_col}{})".format(
                    *table2_range,
                    payment_bonus_col=get_column_letter(i),
                )
                for i, (manager, client_manager_group) in enumerate(
                    shop_group.groupby(by="manager"),
                    start=1 + table2_offset,
                )
                if df.at(
                    client_manager_group["row"][0] - 1, "is_driver"
                )  # I'm not sure but it could be empty
            }
        )

        for r in dataframe_to_rows(table2_header_df, index=False, header=False):
            ws.append(r)
            for cell in list(ws)[-1]:
                cell.style = "subgroup_header_cell"

        for r in dataframe_to_rows(table2_df, index=False, header=False):
            ws.append(r)
            for cell in list(ws)[-1]:
                cell.style = "generic_cell"

        # TABLE 3 CREATION (MANAGERS WITH PAYMENTS)

        table3_df = pd.DataFrame(
            {
                manager: client_manager_group["row"].apply(
                    lambda x: "=ROUND({}, 0)".format(
                        total_payment_bonus["manager"].format(
                            **cols_by_letter,
                            sheet="raw_data",
                            row=x + 1,
                        )
                    )
                )
                for manager, client_manager_group in shop_group.groupby(by="manager")
                if not df.at(
                    client_manager_group["row"][0] - 1, "is_driver"
                )  # I'm not sure but it could be empty
            }
        )

        table3_offset = (
            table2_offset + len(table2_df.columns) + 2 + 1
        )  # absolute offset from spreadsheet
        table3_size = len(table3_df)
        table3_range = (group_rows_start + 1, group_rows_start + table3_size)
        table3_header_df = pd.DataFrame(
            {
                manager: "=SUM({payment_bonus_col}{}:{payment_bonus_col}{})".format(
                    *table3_range,
                    payment_bonus_col=get_column_letter(i),
                )
                for i, (manager, client_manager_group) in enumerate(
                    shop_group.groupby(by="manager"),
                    start=1 + table3_offset,
                )
                if not df.at(
                    client_manager_group["row"][0] - 1, "is_driver"
                )  # I'm not sure but it could be empty
            }
        )

        for r in dataframe_to_rows(table3_header_df, index=False, header=False):
            ws.append(r)
            for cell in list(ws)[-1]:
                cell.style = "subgroup_header_cell"

        for r in dataframe_to_rows(table3_df, index=False, header=False):
            ws.append(r)
            for cell in list(ws)[-1]:
                cell.style = "generic_cell"

        assert (
            table1_size == table2_size
        ), f"table 1 and table 2 are different: {table1_size} and {table2_size} respectively"
        assert (
            table1_size == table3_size
        ), f"table 1 and table 3 are different: {table1_size} and {table3_size} respectively"
        assert (
            table2_size == table3_size
        ), f"table 2 and table 3 are different: {table2_size} and {table3_size} respectively"

        ws.row_dimensions.group(
            group_rows_start + 1,
            group_rows_start + table1_size,
            hidden=True,
            outline_level=1,
        )

        # move to next sub-header row
        group_rows_start += len(table1_header_df) + len(table1_df)
