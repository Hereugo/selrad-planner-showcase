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

