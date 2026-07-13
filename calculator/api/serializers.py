from rest_framework import serializers


class SolarCalculatorSerializer(serializers.Serializer):
    panel_quantity = serializers.IntegerField(min_value=1)
    panel_watt = serializers.ChoiceField(choices=[550, 585, 600])

    frame_quantity = serializers.IntegerField(min_value=1)

    inverter_company = serializers.ChoiceField(
        choices=["Desi", "Galaxy"]
    )

    inverter_capacity = serializers.ChoiceField(
        choices=[8, 10]
    )