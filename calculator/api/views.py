from decimal import Decimal

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    PanelRate,
    FrameRate,
    ElectricalEquipment,
    Inverter,
    Labour,
    InstallmentSetting,
)

from .serializers import SolarCalculatorSerializer


class SolarCalculatorAPIView(APIView):

    def post(self, request):

        serializer = SolarCalculatorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        panel_quantity = serializer.validated_data["panel_quantity"]
        panel_watt = serializer.validated_data["panel_watt"]
        frame_quantity = serializer.validated_data["frame_quantity"]
        inverter_company = serializer.validated_data["inverter_company"]
        inverter_capacity = serializer.validated_data["inverter_capacity"]

        # -----------------------------
        # Panel Rate
        # -----------------------------
        panel_rate = PanelRate.objects.get(
            panel_watt=panel_watt,
            is_active=True
        )

        total_watt = panel_quantity * panel_watt
        panel_price = Decimal(total_watt) * panel_rate.rate_per_watt

        # -----------------------------
        # Frame Rate
        # -----------------------------
        frame_rate = FrameRate.objects.filter(
            is_active=True
        ).first()

        frame_price = (
            Decimal(frame_quantity)
            * frame_rate.rate_per_frame
        )

        # -----------------------------
        # Electrical Equipment
        # -----------------------------
        equipment = ElectricalEquipment.objects.get(
            min_panels__lte=panel_quantity,
            max_panels__gte=panel_quantity,
            is_active=True
        )

        equipment_price = equipment.price

        # -----------------------------
        # Inverter
        # -----------------------------
        inverter = Inverter.objects.get(
            company=inverter_company,
            capacity=inverter_capacity,
            is_active=True
        )

        inverter_price = inverter.price

        # -----------------------------
        # Labour
        # -----------------------------
        labour = Labour.objects.filter(
            is_active=True
        ).first()

        labour_price = labour.electrical_labour

        # -----------------------------
        # Grand Total
        # -----------------------------
        grand_total = (
            panel_price
            + frame_price
            + equipment_price
            + inverter_price
            + labour_price
        )

        # -----------------------------
        # Installment
        # -----------------------------
        installment = InstallmentSetting.objects.get(
            months=12,
            is_active=True
        )

        installment_total = (
            grand_total
            * installment.multiplier
        )

        first_month_payment = (
            installment_total
            * Decimal("0.20")
        )

        remaining_amount = (
            installment_total
            - first_month_payment
        )

        monthly_payment = (
            remaining_amount
            / Decimal("11")
        )

        return Response({

            "panel_price": panel_price,

            "frame_price": frame_price,

            "equipment_price": equipment_price,

            "inverter_price": inverter_price,

            "labour_price": labour_price,

            "grand_total": grand_total,

            "installment_total": installment_total,

            "first_month_payment": first_month_payment,

            "monthly_payment": monthly_payment,

        }, status=status.HTTP_200_OK)