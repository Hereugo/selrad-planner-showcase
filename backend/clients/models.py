import logging

from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import Point

from django.db import models
from django.utils import timezone


logger = logging.getLogger(__name__)


class Client(models.Model):
    """Model Client"""

    name = models.CharField(
        max_length=255, verbose_name="Имя клиента", help_text="Введите имя клиента"
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
    is_hidden_on_map = models.BooleanField(
        verbose_name="Скрыть на карте",
        help_text="Скрыть клиента на карте",
        default=False,
    )

    address = models.ForeignKey(
        "Address",
        on_delete=models.PROTECT,
        related_name="clients",
        verbose_name="Адрес клиента",
        help_text="Выберите адрес клиента",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Save the model instance. Update the updated_at field."""
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        ordering = ["-created_at"]


class Address(gis_models.Model):
    street = models.CharField(
        max_length=255,
        verbose_name="Адрес клиента",
        help_text="Введите адрес клмента",
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
    created_at = models.DateTimeField(
        verbose_name="Дата создания",
        auto_now_add=True,
        editable=False,
    )
    updated_at = models.DateTimeField(
        verbose_name="Дата обновления",
        editable=False,
    )
    point = gis_models.PointField(
        verbose_name="Точка",
        help_text="Точка адреса",
        blank=True,
        null=True,
        spatial_index=True,
    )
    is_overridden = models.BooleanField(
        verbose_name="Перезаписано",
        help_text="Перезаписано",
        default=False,
    )

    def update_coordinates_by_link(self, link=None):
        """Update the coordinates of the address by twogis link."""
        link = link or self.twogis_link

        # TODO:
        # check if the link is a valid 2gis link
        # extract params from the link
        # assign the extracted params to the lat, lon, and point fields
        pass

    def __str__(self):
        return f"{self.pk} | {self.street}"

    def save(self, *args, **kwargs):
        """Save the model instance. Update the updated_at field."""
        self.updated_at = timezone.now()

        if self.is_overridden:
            self.lat = self.point.y
            self.lon = self.point.x

        self.point = Point(float(self.lon or 0), float(self.lat or 0))

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Адрес"
        verbose_name_plural = "Адреса"
        ordering = ["street"]
