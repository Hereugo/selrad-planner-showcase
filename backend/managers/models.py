from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import Point

user = get_user_model()


class GeoPoint(models.Model):
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        verbose_name="Широта",
        help_text="Введите широту адреса",
        default=0,
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        verbose_name="Долгота",
        help_text="Введите долгота адреса",
        default=0,
    )
    accuracy = models.FloatField(
        verbose_name="Точность",
        help_text="Точность координат",
        blank=True,
        null=True,
    )
    speed = models.FloatField(
        verbose_name="Скорость в м/с",
        help_text="Скорость в метрах в секунду",
        blank=True,
        null=True,
    )
    heading = models.FloatField(
        verbose_name="Направление",
        help_text="Направление движения",
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        verbose_name="Дата создания",
        auto_now_add=True,
        editable=False,
    )
    point = gis_models.PointField(
        verbose_name="Точка",
        help_text="Точка адреса",
        blank=True,
        null=True,
        spatial_index=True,
    )
    manager = models.ForeignKey(
        "Manager",
        on_delete=models.SET_NULL,
        related_name="geopoints",
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.pk} | {self.lat} | {self.lon}"

    def save(self, *args, **kwargs):
        """Save the model instance. Update the updated_at field."""
        self.point = Point(float(self.lon), float(self.lat))

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Геоточка"
        verbose_name_plural = "Геоточки"
        ordering = ["-created_at"]


class Manager(models.Model):
    user = models.OneToOneField(
        user,
        on_delete=models.CASCADE,
        related_name="manager",
        blank=True,
        null=True,
    )
    first_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    last_name = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )
    updated_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )
    is_hidden = models.BooleanField(
        default=False,
    )
    roles = models.ManyToManyField(
        "Role",
        through="ManagerRole",
        related_name="managers",
        blank=True,
    )

    def __str__(self):
        if not self.last_name:
            return self.first_name
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        """Save the model instance. Update the updated_at field."""
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Менеджер"
        verbose_name_plural = "Менеджеры"


class Role(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )
    updated_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Save the model instance. Update the updated_at field."""
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Роль"
        verbose_name_plural = "Роли"


class ManagerRole(models.Model):
    manager = models.ForeignKey(
        Manager,
        on_delete=models.CASCADE,
    )
    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )

    def __str__(self):
        return f"{self.manager} | {self.role}"

    class Meta:
        verbose_name = "Роль менеджера"
        verbose_name_plural = "Роли менеджеров"
        unique_together = [["manager", "role"]]
        ordering = ["-created_at"]
