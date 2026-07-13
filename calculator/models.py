from django.db import models
from django.core.validators import MinValueValidator


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# --------------------------------------------------
# Panel Rate
# --------------------------------------------------

class PanelRate(TimeStampedModel):
    panel_watt = models.PositiveIntegerField(
        unique=True,
        help_text="Example: 550, 585, 600"
    )

    rate_per_watt = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["panel_watt"]
        verbose_name = "Panel Rate"
        verbose_name_plural = "Panel Rates"

    def __str__(self):
        return f"{self.panel_watt}W"


# --------------------------------------------------
# Frame Rate
# --------------------------------------------------

class FrameRate(TimeStampedModel):
    rate_per_frame = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Frame Rate"
        verbose_name_plural = "Frame Rate"

    def __str__(self):
        return f"Rs {self.rate_per_frame} Per Frame"


# --------------------------------------------------
# Electrical Equipment
# --------------------------------------------------

class ElectricalEquipment(TimeStampedModel):
    package_name = models.CharField(
        max_length=100,
        blank=True
    )

    min_panels = models.PositiveIntegerField()

    max_panels = models.PositiveIntegerField()

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["min_panels"]
        verbose_name = "Electrical Equipment"
        verbose_name_plural = "Electrical Equipment"

    def __str__(self):
        return f"{self.min_panels}-{self.max_panels} Panels"


# --------------------------------------------------
# Inverter
# --------------------------------------------------

class Inverter(TimeStampedModel):

    DESI = "Desi"
    GALAXY = "Galaxy"

    COMPANY_CHOICES = (
        (DESI, "Desi"),
        (GALAXY, "Galaxy"),
    )

    company = models.CharField(
        max_length=20,
        choices=COMPANY_CHOICES
    )

    capacity = models.PositiveIntegerField(
        help_text="Example: 8 or 10"
    )

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("company", "capacity")
        ordering = ["company", "capacity"]
        verbose_name = "Inverter"
        verbose_name_plural = "Inverters"

    def __str__(self):
        return f"{self.company} {self.capacity}kW"


# --------------------------------------------------
# Labour
# --------------------------------------------------

class Labour(TimeStampedModel):

    electrical_labour = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Electrical Labour"
        verbose_name_plural = "Electrical Labour"

    def __str__(self):
        return f"Rs {self.electrical_labour}"


# --------------------------------------------------
# Installment Setting
# --------------------------------------------------

class InstallmentSetting(TimeStampedModel):

    months = models.PositiveIntegerField(
        default=12,
        unique=True
    )

    multiplier = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(1)]
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Installment Setting"
        verbose_name_plural = "Installment Settings"

    def __str__(self):
        return f"{self.months} Months"