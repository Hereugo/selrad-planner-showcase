# Generated manually for client GPS fix time support.

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("managers", "0027_alter_manager_depot_lat_alter_manager_depot_lon"),
    ]

    operations = [
        migrations.AlterField(
            model_name="geopoint",
            name="created_at",
            field=models.DateTimeField(
                default=django.utils.timezone.now,
                editable=False,
                verbose_name="Дата создания",
            ),
        ),
    ]
