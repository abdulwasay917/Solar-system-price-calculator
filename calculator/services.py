from decimal import Decimal
from django.core.cache import cache

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
    def get_cached_config():
        """
        Calculates rates from cache if available, otherwise queries DB and caches for 1 hour.
        Also caches all Inverters dictionary for fast in-memory lookup.
        """
        config = cache.get("solar_calculator_config")

        if not config:
            # Build an in-memory lookup map for inverters: {(company, capacity): price}
            inverter_map = {}
            for inv in Inverter.objects.all():
                # Hybrid format ya specific company+capacity
                if inv.company == "Hybrid":
                    inverter_map[("Hybrid", None)] = inv.price
                if inv.capacity is not None:
                    inverter_map[(inv.company, inv.capacity)] = inv.price

            config = {
                "panel_rate": PanelRate.objects.first(),
                "frame_rate": FrameRate.objects.first(),
                "equipment": ElectricalEquipment.objects.first(),
                "labour": Labour.objects.first(),
                "installment": InstallmentSetting.objects.first(),
                "inverter_map": inverter_map,
            }

            # Cache configuration for 1 hour (3600 seconds)
            cache.set("solar_calculator_config", config, 3600)

        return config

    @classmethod
    def calculate(
        cls,
        panel_quantity,
        panel_watt,
        frame_quantity,
        inverter_company,
        inverter_capacity,
    ):
        # Fetch cached system setup
        config = cls.get_cached_config()

        # 1. Panel Calculation
        panel_rate = config["panel_rate"]
        if not panel_rate:
            raise Exception("Panel rate not configured")

        total_watt = int(panel_quantity) * int(panel_watt)
        panel_price = Decimal(total_watt) * panel_rate.rate_per_watt

        # 2. Frame Calculation
        frame_rate = config["frame_rate"]
        if not frame_rate:
            raise Exception("Frame rate not configured")

        frame_price = Decimal(frame_quantity) * frame_rate.rate_per_frame

        # 3. Electrical Equipment
        equipment = config["equipment"]
        if not equipment:
            raise Exception("Electrical equipment price not configured")

        # 4. Inverter Calculation
        if inverter_company == "None":
            inverter_price = Decimal("0")

        elif inverter_company == "Hybrid":
            inverter_price = config["inverter_map"].get(("Hybrid", None))
            if inverter_price is None:
                # Fallback to direct query if not present in cache
                try:
                    inverter_price = Inverter.objects.get(company="Hybrid").price
                except Inverter.DoesNotExist:
                    raise Exception("Hybrid inverter not configured")

        else:
            capacity_int = int(inverter_capacity) if inverter_capacity else None
            inverter_price = config["inverter_map"].get((inverter_company, capacity_int))
            if inverter_price is None:
                # Fallback to direct query if cache missed specific entry
                try:
                    inverter_price = Inverter.objects.get(
                        company=inverter_company, capacity=capacity_int
                    ).price
                except Inverter.DoesNotExist:
                    raise Exception(f"Inverter {inverter_company} ({inverter_capacity}kW) not configured")

        # 5. Labour
        labour = config["labour"]
        if not labour:
            raise Exception("Labour price not configured")

        # 6. Grand Total
        grand_total = (
            panel_price
            + frame_price
            + equipment.price
            + inverter_price
            + labour.price
        )

        # 7. Installment
        installment = config["installment"]
        if not installment:
            raise Exception("Installment setting not configured")

        installment_total = grand_total * (
            Decimal("1") + (installment.commission_percentage / Decimal("100"))
        )

        first_month = installment_total * Decimal("0.20")
        monthly_payment = (installment_total - first_month) / Decimal("11")

        return {
            "panel_price": panel_price,
            "frame_price": frame_price,
            "equipment_price": equipment.price,
            "inverter_price": inverter_price,
            "labour_price": labour.price,
            "grand_total": grand_total,
            "installment_total": installment_total,
            "first_month_payment": first_month,
            "monthly_payment": monthly_payment,
        }