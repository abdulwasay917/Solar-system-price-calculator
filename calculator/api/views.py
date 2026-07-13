from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import SolarCalculatorSerializer
from calculator.services import SolarCalculationService


class SolarCalculatorAPIView(APIView):

    def post(self, request):

        serializer = SolarCalculatorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = SolarCalculationService.calculate(
            **serializer.validated_data
        )

        return Response(data)