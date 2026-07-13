from django.db import models


class PanelRate(models.Model):

    rate_per_watt = models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return f"Panel Rate: {self.rate_per_watt}/W"


class FrameRate(models.Model):

    rate_per_frame = models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return f"Frame Rate: {self.rate_per_frame}"


class ElectricalEquipment(models.Model):

    price = models.DecimalField(max_digits=12,decimal_places=2)

    def __str__(self):
        return f"Electrical Equipment: {self.price}"


class Inverter(models.Model):

    COMPANY_CHOICES = (
        ("Desi", "Desi"),
        ("Galaxy", "Galaxy"),
    )

    company = models.CharField(
        max_length=20,
        choices=COMPANY_CHOICES
    )

    capacity = models.PositiveIntegerField()

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