from django.db import migrations

from math import ceil


def default_box_count_for_plan(apps, schema_editor):
    """Set the default value for the box_count field of the Plan model."""
    Plan = apps.get_model("plans", "Plan")
    for plan in Plan.objects.all():
        if plan.box_count is None:
            plan.box_count = ceil(plan.shipment_cost / 100_000)
            plan.save()


class Migration(migrations.Migration):

    dependencies = [
        ("plans", "0006_plan_box_count"),
    ]

    operations = [migrations.RunPython(default_box_count_for_plan)]
