import uuid
from math import ceil

from django.db import models
from django.utils import timezone
from django.urls import reverse


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
    shipment_cost = models.DecimalField(
        verbose_name="Сумма отгрузки",
        help_text="Ввидите сумму отгрузки",
        max_digits=15,
        decimal_places=2,
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
    address = models.ForeignKey(
        "clients.Address",
        verbose_name="Адрес",
        help_text="Выберите адрес",
        related_name="plans",
        on_delete=models.CASCADE,
        null=True,
    )

    def get_absolute_url(self):
        return reverse("plans")

    @property
    def box_count(self):
        """The box count, calculated from the shipment cost."""
        return ceil(self.shipment_cost / 100_000)

    def __str__(self):
        return f"{self.assigned_date}"

    def save(self, *args, **kwargs):
        """Save the model instance. Update the updated_at field."""
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
