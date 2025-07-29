# Author: Amir Nurmukhambetov
# Date: 2024-08-13
#
# The WorkItem model is not defined here because migrating this model to another application can be complex.
# Instead, these are the models that the WorkItem model will reference.
# Each instance of WorkItem includes a content_type, which refers to the specific
# model associated with the WorkItem. Additionally, the content_object is specifically created for PlanWorkItem.
#
# BaseWorkItem contains common fields for all work items, such as completed_by and created_at.

from django.db import models
from django.utils import timezone
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
    time_since_last_box_arrival = models.DateTimeField(
        verbose_name="Время с момента последнего прихода (time since last update on box_count)",
        blank=True,
        null=True,
    )

    class Meta(BaseWorkItem.Meta):
        verbose_name = "Отгрузка"
        verbose_name_plural = "Отгрузки"
        ordering = ("-created_at",)

    def save(self, *args, **kwargs):
        # Check if the instance is already in the database (i.e., update case)
        if self.pk:
            prev_instance = Shipment.objects.get(pk=self.pk)
            if prev_instance.box_count != self.box_count:
                self.time_since_last_box_arrival = timezone.now()

        super().save(*args, **kwargs)


class Return(BaseWorkItem):
    class Meta(BaseWorkItem.Meta):
        verbose_name = "Возврат"
        verbose_name_plural = "Возвраты"
        ordering = ("-created_at",)


def tg_photos_default():
    return {}


class Photo(BaseWorkItem):
    tg_photo_batch_before_message_ids = models.JSONField(
        verbose_name="Обьект id сообщении, где key это id группы альбомы или id фотки, а value это список message_id",
        default=tg_photos_default,
    )
    tg_photo_batch_after_message_ids = models.JSONField(
        verbose_name="Обьект id сообщении, где key это id группы альбомы или id фотки, а value это список message_id",
        default=tg_photos_default,
    )
    tg_from_chat_id = models.CharField(
        max_length=255,
        verbose_name="Чат из которого сообщение были полученны",
        blank=True,
        null=True,
    )

    class Meta(BaseWorkItem.Meta):
        verbose_name = "Фото"
        verbose_name_plural = "Фотки"
        ordering = ("-created_at",)
