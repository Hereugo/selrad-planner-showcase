from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import Point

user = get_user_model()


class GeoPoint(models.Model):
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        verbose_name="Широта",
        help_text="Введите широту адреса",
        default=0,
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        verbose_name="Долгота",
        help_text="Введите долгота адреса",
        default=0,
    )
    accuracy = models.FloatField(
        verbose_name="Точность",
        help_text="Точность координат",
        blank=True,
        null=True,
    )
    speed = models.FloatField(
        verbose_name="Скорость в м/с",
        help_text="Скорость в метрах в секунду",
        blank=True,
        null=True,
    )
    heading = models.FloatField(
        verbose_name="Направление",
        help_text="Направление движения",
        blank=True,
        null=True,
    )
    manager = models.ForeignKey(
        "Manager",
        on_delete=models.CASCADE,
        related_name="geopoints",
        blank=True,
        null=True,
    )
    point = gis_models.PointField(
        verbose_name="Точка",
        help_text="Точка адреса",
        blank=True,
        null=True,
        spatial_index=True,
    )
    created_at = models.DateTimeField(
        verbose_name="Дата создания",
        auto_now_add=True,
        editable=False,
    )

    def __str__(self):
        return f"{self.pk} | {self.latitude} | {self.longitude}"

    def save(self, *args, **kwargs):
        """Save the model instance. Update the updated_at field."""
        self.point = Point(float(self.longitude), float(self.latitude))

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Геоточка"
        verbose_name_plural = "Геоточки"
        ordering = ["-created_at"]


# This Model extends User model
class Manager(models.Model):
    user = models.OneToOneField(
        user,
        on_delete=models.CASCADE,
        related_name="manager",
        blank=True,
        null=True,
    )
    name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    payment = models.IntegerField(
        verbose_name="Выплаты менеджеру в (₸)",
        help_text="Введите выплату менеджеру в (₸)",
        default=0,
    )
    # -============ MANAGER ATTRIBUTES ==============-
    is_hidden = models.BooleanField(
        help_text="Скрыть менеджера", verbose_name="Скрыть", default=False
    )
    is_driver = models.BooleanField(
        help_text="Является ли менеджер водителем",
        verbose_name="Водитель",
        default=False,
    )
    is_warehouser = models.BooleanField(
        help_text="Является ли менеджер кладовщиком",
        verbose_name="Кладовщик",
        default=False,
    )
    is_accountant = models.BooleanField(
        help_text="Является ли менеджер бухгалтером",
        verbose_name="Бухгалтрер",
        default=False,
    )
    is_manager = models.BooleanField(
        help_text="Является ли менеджер менеджером",
        verbose_name="Менеджер",
        default=False,
    )

    def __str__(self):
        name = self.name
        roles = ""
        if self.is_driver:
            roles += Manager.is_driver.field.verbose_name + " "
        if self.is_warehouser:
            roles += Manager.is_warehouser.field.verbose_name + " "
        if self.is_manager:
            roles += Manager.is_manager.field.verbose_name + " "
        if self.is_accountant:
            roles += Manager.is_accountant.field.verbose_name + " "
        return f"{name} | {roles} | {'Скрыт' if self.is_hidden else 'Виден'}"

    class Meta:
        verbose_name = "Менеджер"
        verbose_name_plural = "Менеджеры"
        ordering = ("-pk",)
        permissions = [
            ("view_settings", "Can view settings"),
            ("view_payments_section", "Can view payments section (in settings)"),
        ]
