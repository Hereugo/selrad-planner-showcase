from io import BytesIO
from PIL import Image
from tempfile import TemporaryFile
from datetime import datetime

import pandas as pd
from html2image import Html2Image

from django.db.models import QuerySet

from plans.models import Plan
from managers.models import Manager


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
    }
    for i, plan in enumerate(plans, start=1):
        l["№\nп/п"].append(i)
        l["Клиент"].append(plan.client.name)
        l["Кол-во коробок"].append(plan.box_count)
        l["Место Отгрузки"].append(plan.client.address.street)
        l["Контактное лицо"].append(", ".join([m.name for m in plan.managers.all()]))
        l["Доп информация"].append(plan.comment)

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
        <h1>Диспетчерсктй лист {manager.name}</h1>
        <span>Параметры:</span><br />
        <span>Период: {start_date.strftime("%d.%m.%Y")} с {end_date.strftime("%d.%m.%Y")}</span><br />
        <span>Менеджер: {manager.name}</span><br />
        <br />
        {f.read()}
        <h2>{comment}</h2>
        """

        css_str = "table,th{border:1px solid #000,background-color:white;}*{box-sizing:border-box;font-family:Arial,sans-serif;background-color:white;}table{border-collapse:collapse;width:100%}th{background-color:#d3d3d3;font-size:14px;font-weight:700;text-align:left}td,th{padding:8px}tr th:first-child{width:24px;max-width:24px}tr th:nth-child(2),tr th:nth-child(4){width:300px;max-width:300px}tr th:nth-child(3){width:50px;max-width:50px}tr td:nth-child(3){font-size:20px;font-weight:700;text-align:center}tr th:nth-child(5){width:200px;max-width:200px}tr th:nth-child(6){width:100px;max-width:100px}"

        calc_height = 500 + len(df) * 40

        img = hti.screenshot(
            html_str,
            css_str=css_str,
            save_as="html_table.png",
            size=(1920, calc_height),
        )

        image = Image.open(img[0])
        image.save(buffer, format="png", optimize=True, quality=95)
        buffer.seek(0)

    # delete html_table

    return buffer
