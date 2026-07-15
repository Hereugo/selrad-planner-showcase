from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("managers", "0024_alter_manager_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="manager",
            name="depot_lat",
            field=models.DecimalField(
                decimal_places=6,
                max_digits=9,
                null=True,
                blank=True,
                help_text="Широта домашней точки менеджера",
                verbose_name="Широта депо",
            ),
        ),
        migrations.AddField(
            model_name="manager",
            name="depot_lon",
            field=models.DecimalField(
                decimal_places=6,
                max_digits=9,
                null=True,
                blank=True,
                help_text="Долгота домашней точки менеджера",
                verbose_name="Долгота депо",
            ),
        ),
    ]
