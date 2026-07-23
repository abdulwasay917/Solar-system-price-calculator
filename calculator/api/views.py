from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Correct class name: SolarCalculatorSerializer
from .serializers import SolarCalculatorSerializer
from calculator.services import SolarCalculationService


class SolarCalculatorAPIView(APIView):

    def post(self, request):
        serializer = SolarCalculatorSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        try:
            results = SolarCalculationService.calculate(
                panel_quantity=data.get("panel_quantity", 0),
                panel_watt=data.get("panel_watt", 585),
                frame_quantity=data.get("frame_quantity", 0),
                inverter_company=data.get("inverter_company"),
                inverter_capacity=data.get("inverter_capacity"),
            )
            return Response(results, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )