import re
import logging
from math import ceil

from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError


logger = logging.getLogger(__name__)


def validate_sum_string(value):
    """Validate the sum string."""
    # write a regex expression to validate a string that represents a sum of numbers each number could be a float
    r = r"^[-+]?(\d+(\.\d*)?|\.\d+)(\s*[-+]\s*[-+]?(\d+(\.\d*)?|\.\d+))*$"
    if not re.match(r, value):
        raise ValidationError("Invalid sum string")


class WorkItem(models.Model):
    """Model WorkItem"""

    name = models.CharField(
        verbose_name="Название работы",
        help_text="Введите название работы",
        max_length=255,
    )
    meta_name = models.CharField(
        verbose_name="Мета название работы",
        help_text="Введите мета название работы",
        max_length=255,
        blank=True,
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
    statuses = models.ManyToManyField(
        to="Status",
        verbose_name="Статусы",
        help_text="Выберите статусы",
        related_name="work_items",
        through="WorkItemStatus",
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
    work_items = models.ManyToManyField(
        "WorkItem",
        verbose_name="Список задач для выполнения",
        help_text="Выберите список задач для выполнения",
        through="PlanWorkItem",
        related_name="plans",
    )
    shipment_cost_formula = models.CharField(
        verbose_name="Формула стоимости отгрузки",
        help_text="Введите формулу стоимости отгрузки",
        max_length=255,
        validators=[validate_sum_string],
        default="0",
        null=True,
        blank=True,
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
        cost = self.shipment_cost()
        if self.box_count is None and isinstance(cost, (int, float)):
            self.box_count = ceil(cost / 93_000)
        else:
            self.box_count = 0
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        permissions = [
            ("export_plans", "Can export plans"),
            ("change_old_plan", "Can change old plan"),
            ("delete_old_plan", "Can delete old plan"),
            ("export_report", "Can export report"),
        ]
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


class PlanWorkItem(models.Model):
    """Model PlanWorkItem"""

    work_item = models.ForeignKey(
        "WorkItem",
        on_delete=models.CASCADE,
        verbose_name="Список задач для выполнения",
        help_text="Выберите список задач для выполнения",
    )
    plan = models.ForeignKey(
        "Plan", on_delete=models.CASCADE, verbose_name="План", help_text="Выберите план"
    )
    completed_by = models.ForeignKey(
        "managers.Manager",
        on_delete=models.SET_NULL,
        verbose_name="Менеджер",
        help_text="Выберите менеджера",
        null=True,
        blank=True,
        related_name="completed_plan_worklists",
    )
    status = models.ForeignKey(
        "Status",
        on_delete=models.SET_NULL,
        verbose_name="Статус",
        help_text="Выберите статус",
        null=True,
        blank=True,
    )
    updated_at = models.DateTimeField(
        verbose_name="Дата обновления", editable=False, blank=True, null=True
    )
    created_at = models.DateTimeField(
        verbose_name="Дата создания",
        auto_now_add=True,
        editable=False,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Список задач для выполнения"
        verbose_name_plural = "Списки задач для выполнения"
        ordering = ("-plan", "work_item")

    def save(self, *args, **kwargs):
        """Save the model instance. Update the updated_at field."""
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)


class Status(models.Model):
    """Model Status"""

    name = models.CharField(
        verbose_name="Статус",
        help_text="Введите статус",
        max_length=255,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"
        ordering = ["name"]


class WorkItemStatus(models.Model):
    """Model WorkItemStatus"""

    work_item = models.ForeignKey(
        "WorkItem",
        on_delete=models.CASCADE,
        verbose_name="Список задач для выполнения",
        help_text="Выберите список задач для выполнения",
    )
    status = models.ForeignKey(
        "Status",
        on_delete=models.CASCADE,
        verbose_name="Статус",
        help_text="Выберите статус",
    )

    class Meta:
        verbose_name = "Статус списка задач"
        verbose_name_plural = "Статусы списка задач"
        ordering = ("work_item", "status")
