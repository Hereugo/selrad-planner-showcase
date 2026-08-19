from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("managers", "0025_add_depot_to_manager"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="manager",
            options={
                "ordering": ("-pk",),
                "permissions": [
                    ("view_settings", "Can view settings"),
                    (
                        "view_payments_section",
                        "Can view payments section (in settings)",
                    ),
                    ("can_send_photos_telegram", "Can send photos in telegram"),
                    (
                        "can_preview_photos_telegram",
                        "Can preview photos in telegram",
                    ),
                    ("can_send_old_photos", "Can upload photos on old tasks"),
                    ("can_view_all_tasks", "Can view all tasks"),
                    (
                        "can_receive_photo_notification",
                        "Can receive notification on upload photo",
                    ),
                    ("view_daily_tracking", "Can view daily tracking"),
                ],
                "verbose_name": "Менеджер",
                "verbose_name_plural": "Менеджеры",
            },
        ),
        migrations.AddIndex(
            model_name="geopoint",
            index=models.Index(
                fields=["manager", "created_at"], name="geo_mgr_created_idx"
            ),
        ),
    ]
