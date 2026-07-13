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


        # Panel Calculation

        panel_rate = PanelRate.objects.first()

        if not panel_rate:
            raise Exception("Panel rate not configured")


        total_watt = (
            int(panel_quantity)
            *
            int(panel_watt)
        )


        panel_price = (
            Decimal(total_watt)
            *
            panel_rate.rate_per_watt
        )




        # Frame Calculation

        frame_rate = FrameRate.objects.first()

        if not frame_rate:
            raise Exception("Frame rate not configured")


        frame_price = (
            Decimal(frame_quantity)
            *
            frame_rate.rate_per_frame
        )






        # Electrical Equipment

        equipment = ElectricalEquipment.objects.first()

        if not equipment:
            raise Exception(
                "Electrical equipment price not configured"
            )






        # Inverter Calculation

        # Inverter

        if inverter_company == "None":

            inverter_price = Decimal("0")

        elif inverter_company == "Hybrid":

            inverter = Inverter.objects.get(
                company="Hybrid"
            )

            inverter_price = inverter.price

        else:

            inverter = Inverter.objects.get(
                company=inverter_company,
                capacity=int(inverter_capacity)
            )

            inverter_price = inverter.price








        # Labour

        labour = Labour.objects.first()


        if not labour:
            raise Exception(
                "Labour price not configured"
            )







        # Grand Total

        grand_total = (

            panel_price

            +

            frame_price

            +

            equipment.price

            +

            inverter_price

            +

            labour.price

        )







        # Installment

        installment = InstallmentSetting.objects.first()


        if not installment:
            raise Exception(
                "Installment setting not configured"
            )





        installment_total = (

            grand_total

            *

            (

                Decimal("1")

                +

                (

                    installment.commission_percentage

                    /

                    Decimal("100")

                )

            )

        )





        first_month = (

            installment_total

            *

            Decimal("0.20")

        )





        monthly_payment = (

            installment_total

            -

            first_month

        ) / Decimal("11")







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