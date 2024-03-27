import io
import logging 
from itertools import groupby

import openpyxl
from openpyxl.styles import Border, Side


logger = logging.getLogger(__name__)


COL_DICT = {
    'assigned_date': 1,
    'client': 2,
    'address': 3,
    'manager': 4,
    'worklist': 5,
    'comment': 6,
    'shipment_cost': 7,
    'box_count': 8
}


def generate_excelsheet_by_plan(plans):
    workbook = openpyxl.load_workbook('./static/docs/standard_plan.xlsx')
    ws = workbook.active

    if 'assigned_date_cell' not in workbook.style_names:
        date_style = openpyxl.styles.NamedStyle(name='assigned_date_cell')
        # set format to date with weekday
        date_style.number_format = 'DD.MM.YYYY'

        # font color white, background color gray and bold
        date_style.font = openpyxl.styles.Font(color='FFFFFF', bold=True)
        date_style.fill = openpyxl.styles.PatternFill(
            start_color='808080', end_color='808080', fill_type='solid')
        date_style.alignment = openpyxl.styles.Alignment(
            horizontal='center', vertical='center')
        date_style.alignment.wrap_text = True

        workbook.add_named_style(date_style)

    if 'general_style' not in workbook.style_names:
        general_style = openpyxl.styles.NamedStyle(name='general_style')
        general_style.alignment.wrap_text = True

        general_style.border = Border(left=Side(style='thin'),
                                      right=Side(style='thin'),
                                      top=Side(style='thin'),
                                      bottom=Side(style='thin'))

        workbook.add_named_style(general_style)

    earliest_date = plans.earliest('assigned_date').assigned_date
    latest_date = plans.latest('assigned_date').assigned_date

    ws.cell(row=1, column=1).value = f'Планы на {earliest_date} - {latest_date}'
    ws.cell(row=1, column=1).style = 'assigned_date_cell'

    row = 2
    for assigned_date, plans_by_day in groupby(plans, key=lambda p: p.assigned_date):
        for i, plan in enumerate(plans_by_day, start=1):
            ws.cell(row=row + i, column=COL_DICT['client']).value = plan.client.name
            ws.cell(row=row + i, column=COL_DICT['address']).value = plan.address.street
            ws.cell(row=row + i, column=COL_DICT['manager']).value = ', '.join(
                [str(m) for m in plan.managers.all()])
            ws.cell(row=row + i, column=COL_DICT['worklist']).value = ', '.join(
                [str(w) for w in plan.worklist.all()])
            ws.cell(row=row + i,
                    column=COL_DICT['comment']).value = plan.comment
            ws.cell(
                row=row + i, column=COL_DICT['shipment_cost']).value = plan.shipment_cost
            ws.cell(row=row + i,
                    column=COL_DICT['box_count']).value = plan.box_count

            # apply the general style to the row
            for col in range(2, 9):
                ws.cell(row=row + i, column=col).style = 'general_style'

        x = plans.filter(assigned_date=assigned_date).count() + 1
        ws.merge_cells(start_row=row, start_column=1,
                       end_row=row + x, end_column=1)
        ws.cell(row=row, column=1).value = assigned_date
        ws.cell(row=row, column=1).style = 'assigned_date_cell'

        row += x + 1

    buffer = io.BytesIO()
    workbook.save(buffer)

    return buffer


def generate_excelsheet_by_manager(plans):
    workbook = openpyxl.load_workbook('./static/docs/standard_plan_by_manager.xlsx')
    ws = workbook.active

    if 'assigned_date_cell' not in workbook.style_names:
        date_style = openpyxl.styles.NamedStyle(name='assigned_date_cell')
        # set format to date with weekday
        date_style.number_format = 'DD.MM.YYYY'

        # font color white, background color gray and bold
        date_style.font = openpyxl.styles.Font(color='FFFFFF', bold=True)
        date_style.fill = openpyxl.styles.PatternFill(
            start_color='808080', end_color='808080', fill_type='solid')
        date_style.alignment = openpyxl.styles.Alignment(
            horizontal='center', vertical='center')
        date_style.alignment.wrap_text = True

        workbook.add_named_style(date_style)

    if 'general_style' not in workbook.style_names:
        general_style = openpyxl.styles.NamedStyle(name='general_style')
        general_style.alignment.wrap_text = True

        general_style.border = Border(left=Side(style='thin'),
                                      right=Side(style='thin'),
                                      top=Side(style='thin'),
                                      bottom=Side(style='thin'))

        workbook.add_named_style(general_style)

    earliest_date = plans.earliest('assigned_date').assigned_date
    latest_date = plans.latest('assigned_date').assigned_date

    ws.cell(row=1, column=1).value = f'Отчет на {earliest_date} - {latest_date}'
    ws.cell(row=1, column=1).style = 'assigned_date_cell'

    row = 2
    for assigned_date, plans_by_day in groupby(plans, key=lambda p: p.assigned_date):
        for i, plan in enumerate(plans_by_day, start=1):
            ws.cell(row=row + i, column=COL_DICT['client']).value = plan.client.name
            ws.cell(row=row + i, column=COL_DICT['address']).value = plan.address.street
            ws.cell(row=row + i, column=COL_DICT['manager']).value = ', '.join(
                [str(m) for m in plan.managers.all()])
            ws.cell(row=row + i, column=COL_DICT['worklist']).value = ', '.join(
                [str(w) for w in plan.worklist.all()])
            ws.cell(row=row + i,
                    column=COL_DICT['comment']).value = plan.comment
            ws.cell(
                row=row + i, column=COL_DICT['shipment_cost']).value = plan.shipment_cost
            ws.cell(row=row + i,
                    column=COL_DICT['box_count']).value = plan.box_count

            # apply the general style to the row
            for col in range(2, 9):
                ws.cell(row=row + i, column=col).style = 'general_style'

        x = plans.filter(assigned_date=assigned_date).count() + 1
        ws.merge_cells(start_row=row, start_column=1,
                       end_row=row + x, end_column=1)
        ws.cell(row=row, column=1).value = assigned_date
        ws.cell(row=row, column=1).style = 'assigned_date_cell'

        row += x + 1

    buffer = io.BytesIO()
    workbook.save(buffer)

    return buffer

