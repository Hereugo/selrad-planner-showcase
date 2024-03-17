from django.db import models
from django.utils import timezone

class Client(models.Model):
    """Model Client"""

    name = models.CharField(
        max_length=255,
        verbose_name='Имя клиента',
        help_text='Введите имя клиента'
    )
    address = models.CharField(
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

