import uuid
from django.db import models
from django.utils import timezone

class Plan(models.Model):
    """Model Plan"""

    # TODO: Check for proper translations and find better words that are applicable
    # in our case.
    WORKLIST = (
        ('shipment', 'отгрузка'),
        ('layout', 'выкладка'),
        ('photo', 'фото'),
        ('refund', 'возврат'),
        ('other', 'прочее')
    ) 

    uuid = models.UUIDField(
        verbose_name='UUID',
        primary_key=True,
        editable=False,
        unique=True,
        blank=False,
        null=False
    )
    assigned_date = models.DateField(
        max_length=255,
        verbose_name='Время назначения',
        help_text='Выберите время назначения',
    )
    # TODO: Change to make possible to select multiple values.
    worklist = models.CharField(
        choices=WORKLIST,
        verbose_name='Список задач для выполнения',
        help_text='Выберите список задач для выполнения',
        max_length=255,
    )
    shipment_cost = models.DecimalField(
        verbose_name='Сумма отгрузки',
        help_text='Ввидите сумму отгрузки',
        max_digits=10,
        decimal_places=2,
    )
    is_completed = models.BooleanField(
        verbose_name='Статус выполнения',
        help_text='Отметьте, если план выполнен',
        default=False,
    )
    comment = models.TextField(
        verbose_name='Комментарии',
        help_text='Ввидите доп комментарии',
        blank=True,
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

    managers = models.ManyToManyField(
        'managers.Manager',
        verbose_name='Менеджеры плана',
        help_text='Выберите менеджеров для плана',
        through='PlanManager',
        related_name='plans',
    )
    client = models.ForeignKey(
        'clients.Client',
        verbose_name='Клиент',
        help_text='Выберите клиента',
        related_name='plans',
        on_delete=models.DO_NOTHING,
        null=True,
    )

    @property
    def box_count(self):
        """The box count, calculated from the shipment cost."""
        # TODO implement the box count calculation
        return -1

    def __str__(self):
        return f'{self.assigned_date} - {self.is_completed} - {self.managers}' 

    def save(self, *args, **kwargs):
        """Save the model instance. Update the updated_at field."""
        self.updated_at = timezone.now()
        if not self.uuid:
            self.uuid = uuid.uuid4()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'План'
        verbose_name_plural = 'Планы'
        ordering = ['-assigned_date', '-created_at']


class PlanManager(models.Model):
    """Model PlanManager"""
    manager = models.ForeignKey(
        'managers.Manager',
        on_delete=models.DO_NOTHING,
        verbose_name='Менеджер',
        help_text='Выберите менеджера'
    )
    plan = models.ForeignKey(
        'Plan',
        on_delete=models.DO_NOTHING,
        verbose_name='План',
        help_text='Выберите план'
    )
    created_at = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True
    )

