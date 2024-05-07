import re
import uuid
from math import ceil

from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.core.validators import ValidationError


def validate_sum_string(value):
    """Validate the sum string."""
    # write a regex expression to validate a string that represents a sum of numbers each number could be a float
    r = r"^[-+]?(\d+(\.\d*)?|\.\d+)(\s*[-+]\s*[-+]?(\d+(\.\d*)?|\.\d+))*$"
    if not re.match(r, value):
        raise ValidationError("Invalid sum string")


class Worklist(models.Model):
    """Model Worklist"""

    name = models.CharField(
        verbose_name="Название работы",
        help_text="Введите название работы",
        max_length=255,
    )
    description = models.TextField(
        verbose_name="Описание работы",
        help_text="Введите описание работы",
        blank=True,
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
        verbose_name = "Список задач для выполнения"
        verbose_name_plural = "Списки задач для выполнения"
        ordering = ("-created_at",)


class Plan(models.Model):
    """Model Plan"""

    assigned_date = models.DateField(
        max_length=255,
        verbose_name="Время назначения",
        help_text="Выберите время назначения",
    )
    worklist = models.ManyToManyField(
        "Worklist",
        verbose_name="Список задач для выполнения",
        help_text="Выберите список задач для выполнения",
        through="PlanWorklist",
        related_name="plans",
    )
    shipment_cost_formula = models.CharField(
        verbose_name="Формула стоимости отгрузки",
        help_text="Введите формулу стоимости отгрузки",
        max_length=255,
        validators=[validate_sum_string],
        default="",
        blank=True,
        null=True,
    )
    comment = models.TextField(
        verbose_name="Комментарии",
        help_text="Ввидите доп комментарии",
        blank=True,
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

    managers = models.ManyToManyField(
        "managers.Manager",
        verbose_name="Менеджеры плана",
        help_text="Выберите менеджеров для плана",
        through="PlanManager",
        related_name="plans",
    )
    client = models.ForeignKey(
        "clients.Client",
        verbose_name="Клиент",
        help_text="Выберите клиента",
        related_name="plans",
        on_delete=models.CASCADE,
        null=True,
    )
    box_count = models.IntegerField(
        verbose_name="Количество коробок",
        help_text="Введите количество коробок",
        blank=True,
        null=True,
    )

    def shipment_cost(self):
        try:
            sum = eval(self.shipment_cost_formula)
        except Exception as e:
            logger.error(f"Error while evaluating formula: {e}")
            sum = "Ошибка при вычислении"
        return sum

    def __str__(self):
        return f"{self.assigned_date}"

    def save(self, *args, **kwargs):
        """Save the model instance. Update the updated_at field."""
        if self.box_count is None:
            self.box_count = ceil(self.shipment_cost / 100_000)

        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "План"
        verbose_name_plural = "Планы"
        ordering = ["assigned_date", "-created_at"]


class PlanManager(models.Model):
    """Model PlanManager"""

    manager = models.ForeignKey(
        "managers.Manager",
        on_delete=models.CASCADE,
        verbose_name="Менеджер",
        help_text="Выберите менеджера",
    )
    plan = models.ForeignKey(
        "Plan", on_delete=models.CASCADE, verbose_name="План", help_text="Выберите план"
    )

    class Meta:
        verbose_name = "Менеджер плана"
        verbose_name_plural = "Менеджеры плана"
        ordering = ("plan", "manager")


class PlanWorklist(models.Model):
    """Model PlanWorklist"""

    worklist = models.ForeignKey(
        "Worklist",
        on_delete=models.CASCADE,
        verbose_name="Список задач для выполнения",
        help_text="Выберите список задач для выполнения",
    )
    plan = models.ForeignKey(
        "Plan", on_delete=models.CASCADE, verbose_name="План", help_text="Выберите план"
    )

    class Meta:
        verbose_name = "Список задач для выполнения"
        verbose_name_plural = "Списки задач для выполнения"
        ordering = ("plan", "worklist")
