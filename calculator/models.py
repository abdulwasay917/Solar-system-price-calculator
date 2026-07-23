from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache


class PanelRate(models.Model):

    rate_per_watt = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Panel Rate: {self.rate_per_watt}/W"


class FrameRate(models.Model):

    rate_per_frame = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Frame Rate: {self.rate_per_frame}"


class ElectricalEquipment(models.Model):

    price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"Electrical Equipment: {self.price}"


class Inverter(models.Model):

    COMPANY_CHOICES = (
        ("None", "None"),
        ("Desi", "Desi"),
        ("Galaxy", "Galaxy"),
        ("Hybrid", "Hybrid"),
    )

    company = models.CharField(
        max_length=20,
        choices=COMPANY_CHOICES
    )

    capacity = models.PositiveIntegerField(null=True, blank=True)

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    class Meta:
        unique_together = (
            "company",
            "capacity"
        )

    def __str__(self):
        return f"{self.company} {self.capacity}kW"


class Labour(models.Model):

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    def __str__(self):
        return f"Labour: {self.price}"


class InstallmentSetting(models.Model):

    commission_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=40
    )

    installment_multiplier = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=1.4
    )

    def __str__(self):
        return "Installment Settings"


# --- AUTOMATIC CACHE CLEARING SIGNALS ---
@receiver([post_save, post_delete], sender=PanelRate)
@receiver([post_save, post_delete], sender=FrameRate)
@receiver([post_save, post_delete], sender=ElectricalEquipment)
@receiver([post_save, post_delete], sender=Inverter)
@receiver([post_save, post_delete], sender=Labour)
@receiver([post_save, post_delete], sender=InstallmentSetting)
def clear_solar_calculator_cache(sender, **kwargs):
    cache.delete("solar_calculator_config")