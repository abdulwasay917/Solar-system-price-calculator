from django.contrib import admin

from .models import (
    PanelRate,
    FrameRate,
    ElectricalEquipment,
    Inverter,
    Labour,
    InstallmentSetting,
)


@admin.register(PanelRate)
class PanelRateAdmin(admin.ModelAdmin):

    list_display = (
        "rate_per_watt",
    )


@admin.register(FrameRate)
class FrameRateAdmin(admin.ModelAdmin):

    list_display = (
        "rate_per_frame",
    )


@admin.register(ElectricalEquipment)
class ElectricalEquipmentAdmin(admin.ModelAdmin):

    list_display = (
        "price",
    )


@admin.register(Inverter)
class InverterAdmin(admin.ModelAdmin):

    list_display = (
        "company",
        "capacity",
        "price",
    )

    list_filter = (
        "company",
        "capacity",
    )


@admin.register(Labour)
class LabourAdmin(admin.ModelAdmin):

    list_display = (
        "price",
    )


@admin.register(InstallmentSetting)
class InstallmentSettingAdmin(admin.ModelAdmin):

    list_display = (
        "commission_percentage",
        "installment_multiplier",
    )