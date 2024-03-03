from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone

PHONE_VALIDATOR = RegexValidator(
    regex=r'^\+?1?\d{9,15}$', 
    message='Номер телефона необходимо ввести в формате: "+9999999999". Допускается до 15 цифр'
)

class Manager(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(
        unique=True,
        blank=True,
        null=True,
    )
    phone_number = models.CharField(
        validators=[
            PHONE_VALIDATOR,
        ],
        max_length=17,
        unique=True,
        blank=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):
        """Save the model instance. Update the updated_at field."""
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Менеджер'
        verbose_name_plural = 'Менеджеры'

