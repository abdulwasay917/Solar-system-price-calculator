from decimal import Decimal

from .models import (
    PanelRate,
    FrameRate,
    ElectricalEquipment,
    Inverter,
    Labour,
    InstallmentSetting,
)


class SolarCalculationService:

    @staticmethod
    def calculate(
        panel_quantity,
        panel_watt,
        frame_quantity,
        inverter_company,
        inverter_capacity,
    ):

        panel_rate = PanelRate.objects.get(
            panel_watt=panel_watt,
            is_active=True
        )

        total_watt = panel_quantity * panel_watt

        panel_price = Decimal(total_watt) * panel_rate.rate_per_watt

        frame_rate = FrameRate.objects.filter(
            is_active=True
        ).first()

        frame_price = (
            Decimal(frame_quantity)
            * frame_rate.rate_per_frame
        )

        equipment = ElectricalEquipment.objects.get(
            min_panels__lte=panel_quantity,
            max_panels__gte=panel_quantity,
            is_active=True
        )

        inverter = Inverter.objects.get(
            company=inverter_company,
            capacity=inverter_capacity,
            is_active=True
        )

        labour = Labour.objects.filter(
            is_active=True
        ).first()

        grand_total = (
            panel_price
            + frame_price
            + equipment.price
            + inverter.price
            + labour.electrical_labour
        )

        installment = InstallmentSetting.objects.get(
            months=12,
            is_active=True
        )

        installment_total = (
            grand_total
            * installment.multiplier
        )

        first_month = installment_total * Decimal("0.20")

        monthly = (
            installment_total - first_month
        ) / Decimal("11")

        return {
            "panel_price": panel_price,
            "frame_price": frame_price,
            "equipment_price": equipment.price,
            "inverter_price": inverter.price,
            "labour_price": labour.electrical_labour,
            "grand_total": grand_total,
            "installment_total": installment_total,
            "first_month_payment": first_month,
            "monthly_payment": monthly,
        }