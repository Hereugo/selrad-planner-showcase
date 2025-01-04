import logging
import re
from math import ceil

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from work_items.models import BaseWorkItem

logger = logging.getLogger(__name__)


def validate_sum_string(value):
    """Validate the sum string."""
    # write a regex expression to validate a string that represents a sum of numbers each number could be a float
    r = r"^[-+]?(\d+(\.\d*)?|\.\d+)(\s*[-+]\s*[-+]?(\d+(\.\d*)?|\.\d+))*$"
    if not re.match(r, value):
        raise ValidationError("Invalid sum string")


class PaymentRegistry(models.Model):
    """Payment registry"""

    date = models.DateField(
        max_length=255,
        verbose_name="Дата совершенного плана",
        help_text="Выберите совершенного плана",
    )
    manager = models.ForeignKey(
        to="managers.Manager",
        verbose_name="Менеджер",
        help_text="Выберите менеджера",
        related_name="payment_registries",
        on_delete=models.CASCADE,
    )
    payment = models.IntegerField(
        verbose_name="Выплаты менеджеру в (₸)",
        help_text="Введите выплату менеджеру в (₸)",
        blank=True,
        null=True,
    )
    bonus = models.IntegerField(
        verbose_name="Бонус менеджеру в (₸)",
        help_text="Введите бонус менеджеру в (₸)",
        blank=True,
        null=True,
        default=0,
    )
    comment = models.TextField(
        verbose_name="Комментарии",
        help_text="Ввидите комментарии",
        blank=True,
    )
    is_confirmed = models.BooleanField(
        verbose_name="Подтвержденно",
        help_text="Подтвержден ли план",
        default=False,
    )

    def plans(self):
        return self.manager.plans.filter(assigned_date=self.date)

    class Meta:
        verbose_name = "Данные о выплате"
        verbose_name_plural = "Реестр выплаты"
        constraints = [
            models.UniqueConstraint(
                fields=["date", "manager"], name="unique_date_manager"
            )
        ]
        ordering = ("-date", "-manager")


class WorkItem(models.Model):
    """Model WorkItem"""

    # https://www.reddit.com/r/django/comments/103uufa/can_you_limit_the_list_of_entities_to_associate/
    target_limit = models.Q(app_label="work_items", model="shipment") | models.Q(
        app_label="work_items", model="return"
    )

    name = models.CharField(
        verbose_name="Название работы",
        help_text="Введите название работы",
        max_length=255,
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to=target_limit,
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(
        verbose_name="Дата создания",
        auto_now_add=True,
        editable=False,
    )

    def __str__(self):
        return f"{self.name} | {self.content_type.model_class().__name__ if self.content_type else '--пусто--'}"

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
    time_since_first_dispatch = models.DateTimeField(
        verbose_name="Время с момента первой отправки диспетчерского листа",
        blank=True,
        null=True,
    )
    is_permanent = models.BooleanField(
        verbose_name="перманентный план",
        help_text="перманентный план",
        default=False,
    )

    invoice_date = models.DateField(
        max_length=255,
        verbose_name="Время Бухгалтера",
        help_text="Выберите время бухгалтера",
        blank=True,
        null=True,
    )
    accountant_comment = models.TextField(
        verbose_name="Комментарии бухгалтера",
        help_text="Ввидите бухгалтера комментарии",
        blank=True,
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
        if self.box_count is None:
            # if isinstance(cost, (int, float)):
            #     self.box_count = ceil(cost / 93_000)
            # else:
            self.box_count = 0

        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        permissions = [
            ("export_plans", "Can export plans"),
            ("add_old_plan", "Can add old plan"),
            ("change_old_plan", "Can change old plan"),
            ("delete_old_plan", "Can delete old plan"),
            ("export_report", "Can export report"),
            ("get_dispatch_list", "Can export dispatch list"),
            ("get_dispatch_report", "Can export dispatch report"),
            ("export_payment_report", "Can export payment report"),
        ]
        verbose_name = "План"
        verbose_name_plural = "Планы"
        ordering = ["-assigned_date", "-created_at"]


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
        constraints = [
            models.UniqueConstraint(
                fields=["plan", "manager"],
                name="unique_plan_manager",
            )
        ]


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

    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, blank=True, null=True
    )
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey("content_type", "object_id")

    def save(self, *args, **kwargs):
        # content_type assigned from work_item because it cannot be referenced
        # directly in GenericForeignKey field.

        # This is only for Admin panel case.
        # Since PlanWorkItem is created in bulk_create, and doesnt call save method.
        if self.work_item.content_type != None and self.content_object == None:
            model_class: BaseWorkItem = self.work_item.content_type.model_class()

            self.content_object = model_class.objects.create(
                work_item=self.work_item,
            )

        return super().save(*args, **kwargs)

    class Meta:
        indexes = [
            models.Index(fields=["plan", "work_item"]),
            models.Index(fields=["content_type", "object_id"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["plan", "work_item"],
                name="unique_plan_work_item",
            )
        ]
