from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0007_address_point'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            update clients_address
            set point = ST_SetSRID(
                ST_MakePoint(
                    lon, lat
                ),
                4326
            );""",
            reverse_sql=migrations.RunSQL.noop,
        )
    ]
