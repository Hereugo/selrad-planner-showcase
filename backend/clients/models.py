from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import Point

from django.db import models
from django.utils import timezone


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

