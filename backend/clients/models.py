import requests
import logging

from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import Point
from django.conf import settings

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

    addresses = models.ManyToManyField(
        "Address",
        through="ClientAddress",
        related_name="clients",
        verbose_name="Адреса клиента",
        help_text="Выберите адреса клиента",
        blank=True,
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

    def update_coordinates(self):
        """Update the coordinates of the address"""
        street = self.street + " г. Алматы, Казахстан"
        street = street.replace("^[A-Za-zА-Яа-яЁё.,]", " ")

        if street is None:
            return

        params = {
            "apikey": settings.YANDEX_API_KEY,
            "geocode": street,
            "format": "json",
            "lang": "ru_RU",
        }

        response = requests.get(settings.YANDEX_API_URL, params=params)

        data = response.json()
        if "response" in data:
            try:
                lon, lat = map(
                    float,
                    data["response"]["GeoObjectCollection"]["featureMember"][0][
                        "GeoObject"
                    ]["Point"]["pos"].split(" "),
                )
                if lon and lat:
                    if not self.lat or not self.lon:
                        logger.info("Location is empty for", street, "new:", lon, lat)
                        self.point = Point(lon, lat, srid=4326)
                    elif (
                        abs(lat - float(self.lat)) > 0.0001
                        or abs(lon - float(self.lon)) > 0.0001
                    ):
                        logger.info(
                            "Location is different for",
                            street,
                            "old:",
                            self.lon,
                            self.lat,
                            "new:",
                            lon,
                            lat,
                        )
                        self.point = Point(lon, lat, srid=4326)

            except Exception as e:
                logger.error(
                    f"Error while updating coordinates for {street}. Error: {e}"
                )

    def __str__(self):
        return f"{self.street} - {self.lat}, {self.lon}"

    def save(self, *args, **kwargs):
        """Save the model instance. Update the updated_at field."""
        self.updated_at = timezone.now()

        if not self.point: 
            self.update_coordinates()

        self.lon = float(self.point.x)
        self.lat = float(self.point.y)

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Адрес"
        verbose_name_plural = "Адреса"
        ordering = ["street"]


class ClientAddress(models.Model):
    """Model ClientAddress"""

    client = models.ForeignKey(
        "Client",
        on_delete=models.CASCADE,
        related_name="client_addresses",
        verbose_name="Клиент",
        help_text="Выберите клиента",
    )
    address = models.ForeignKey(
        "Address",
        on_delete=models.CASCADE,
        related_name="client_addresses",
        verbose_name="Адрес",
        help_text="Выберите адрес",
    )

    def __str__(self):
        return f"{self.client.name} - {self.address.street}"

    class Meta:
        verbose_name = "Адрес клиента"
        verbose_name_plural = "Адреса клиентов"
        ordering = ["client__name"]
