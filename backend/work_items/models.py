# Author: Amir Nurmukhambetov
# Date: 2024-08-13
#
# The WorkItem model is not defined here because migrating this model to another application can be complex.
# Instead, these are the models that the WorkItem model will reference.
# Each instance of WorkItem includes a content_type, which refers to the specific
# model associated with the WorkItem. Additionally, the content_object is specifically created for PlanWorkItem.
#
# BaseWorkItem contains common fields for all work items, such as completed_by and created_at.

from django.utils import timezone
from django.db import models
from polymorphic.models import PolymorphicModel


class BaseWorkItem(PolymorphicModel):
    completed_by = models.ForeignKey(
        "managers.Manager",
        on_delete=models.SET_NULL,
        verbose_name="Менеджер",
        help_text="Выберите менеджера который выполнил",
        null=True,
        blank=True,
        related_name="completed_work_items",
    )
    work_item = models.ForeignKey(
        "plans.WorkItem",
        verbose_name="Список задач для выполнения",
        help_text="Выберите список задач для выполнения",
        on_delete=models.CASCADE,
        related_name="+",
    )
    updated_at = models.DateTimeField(
        verbose_name="Дата обновления",
        auto_now=True,
        editable=False,
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(
        verbose_name="Дата создания",
        auto_now_add=True,
        editable=False,
        blank=True,
        null=True,
    )

    class Meta(PolymorphicModel.Meta):
        verbose_name = "Базовый элемент работы"
        verbose_name_plural = "Базовые элементы работы"
        ordering = ("-created_at",)

    def save(self, *args, **kwargs):
        """Save the model instance. Update the updated_at field."""
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)


class Shipment(BaseWorkItem):
    CHOICES = (
        ("print", "Печать"),
        ("redoing", "Переделка"),
        ("other", "Прочее"),
    )

    box_count = models.IntegerField(
        blank=True,
        null=True,
    )
    status = models.CharField(max_length=10, choices=CHOICES, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    class Meta(BaseWorkItem.Meta):
        verbose_name = "Отгрузка"
        verbose_name_plural = "Отгрузки"
        ordering = ("-created_at",)
