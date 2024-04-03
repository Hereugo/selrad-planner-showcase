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
        max_length=255,
        verbose_name='Имя клиента',
        help_text='Введите имя клиента'
    )
    created_at = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True,
        editable=False,
    )
    updated_at = models.DateTimeField(
        verbose_name='Дата обновления',
        editable=False,
    )

    address = models.ForeignKey(
        'Address',
        on_delete=models.CASCADE,
        related_name='addresses',
        verbose_name='Адрес клиента',
        help_text='Выберите адрес клиента',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name 
    
    def save(self, *args, **kwargs):
        """Save the model instance. Update the updated_at field."""
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ['-created_at']


class Address(gis_models.Model):
    street = models.CharField(
        max_length=255,
        verbose_name='Адрес клиента',
        help_text='Введите адрес клмента',
    )
    lat = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        verbose_name='Широта',
        help_text='Введите широту адреса',
        default=0,
    )
    lon = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        verbose_name='Долгота',
        help_text='Введите долгота адреса',
        default=0,
    )
    created_at = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True,
        editable=False,
    )
    updated_at = models.DateTimeField(
        verbose_name='Дата обновления',
        editable=False,
    )

    point = gis_models.PointField(
        verbose_name='Точка',
        help_text='Точка адреса',
        blank=True,
        null=True,
        spatial_index=True
    )

    def update_coordinates(self):
        """Update the coordinates of the address"""
        street = self.street + 'г. Алматы, Казахстан'
        street = street.replace('^[A-Za-zА-Яа-яЁё.,]', ' ')

        if street is None:
            return 

        params = {
            'address': street,
            'key': settings.GMAPS_API_KEY,
        }
        response = requests.get(settings.GMAPS_API_URL, params=params)
        data = response.json()
        if data['status'] == 'OK':
            location = data['results'][0]['geometry']['location']
            if location:
                if not self.lat or not self.lon:
                    logger.info('Location is empty for', street, 
                          'new:', location['lat'], location['lng'])
                    self.lat, self.lon = float(location['lat']), float(location['lng'])
                elif abs(float(location['lat']) - float(self.lat)) > 0.0001 or abs(float(location['lng']) - float(self.lon)) > 0.0001:
                    logger.info('Location is different for', street, 
                          'old:', self.lat, self.lon, 
                          'new:', location['lat'], location['lng'])
                    self.lat, self.lon = float(location['lat']), float(location['lng'])

            self.save()
        else:
            return

    def __str__(self):
        return f'{self.street} - {self.lat}, {self.lon}'
    
    def save(self, *args, **kwargs):
        """Save the model instance. Update the updated_at field."""
        self.updated_at = timezone.now()
        if self.lon and self.lat:
            self.point = Point(
                float(self.lon),
                float(self.lat),
                srid=4326
            )
        else:
            self.point = None

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'
        ordering = ['street']

