import logging

from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import Point

from django.db import models
from django.utils import timezone


logger = logging.getLogger(__name__)


# This is a client
class MetaClient(models.Model):
    name = models.CharField(
        max_length=255, verbose_name="Имя клиента", help_text="Введите имя клиента"
    )
    created_at = models.DateTimeField(
        verbose_name="Дата создания",
        auto_now_add=True,
        editable=False,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        ordering = ["-created_at"]


# This is a shop client
# TODO: Rename this model to Shop
class Client(models.Model):
    """Model Client"""

    meta_client = models.ForeignKey(
        to=MetaClient,
        related_name="clients",
        verbose_name="Клиент",
        help_text="Выберите клиента к магазину",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    name = models.CharField(
        max_length=255, verbose_name="Имя магазина", help_text="Введите имя магазина"
    )
    address = models.ForeignKey(
        "Address",
        on_delete=models.PROTECT,
        related_name="clients",
        verbose_name="Адрес магазина",
        help_text="Выберите адрес магазина",
        blank=True,
        null=True,
    )
    is_hidden_on_map = models.BooleanField(
        verbose_name="Скрыть на карте",
        help_text="Скрыть магазин на карте",
        default=False,
    )

    created_at = models.DateTimeField(
        verbose_name="Дата создания",
        auto_now_add=True,
        editable=False,
    )
    updated_at = models.DateTimeField(
        verbose_name="Дата обновления",
        editable=False,
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Save the model instance. Update the updated_at field."""
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        permissions = [
            ("export_compare_years", "Can export compare report"),
        ]
        verbose_name = "Магазин"
        verbose_name_plural = "Магазины"
        ordering = ["-created_at"]


class Address(gis_models.Model):
    street = models.CharField(
        max_length=255,
        verbose_name="Адрес магазина",
        help_text="Введите адрес магазина",
    )
    twogis_link = models.CharField(
        max_length=255,
        verbose_name="Ссылка на 2gis",
        help_text="Введите ссылку на 2gis",
        blank=True,
        null=True,
    )
    lat = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        verbose_name="Широта",
        help_text="Введите широту адреса",
        default=0,
    )
    lon = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        verbose_name="Долгота",
        help_text="Введите долгота адреса",
        default=0,
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
    updated_at = models.DateTimeField(
        verbose_name="Дата обновления",
        editable=False,
    )

    def __str__(self):
        return f"{self.pk} | {self.street} | {self.lat} | {self.lon}"

    def save(self, *args, **kwargs):
        """Save the model instance. Update the updated_at field."""
        self.updated_at = timezone.now()
        self.point = Point(float(self.lon or 0), float(self.lat or 0))
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Адрес"
        verbose_name_plural = "Адреса"
        ordering = ["-created_at"]
