from rest_framework import serializers


class SolarCalculatorSerializer(serializers.Serializer):

    panel_quantity = serializers.IntegerField(
        min_value=1
    )


    panel_watt = serializers.ChoiceField(
        choices=[550, 585, 600]
    )


    frame_quantity = serializers.IntegerField(
        min_value=1
    )


    inverter_company = serializers.ChoiceField(
        choices=[
            "Desi",
            "Galaxy",
            "Hybrid"
        ]
    )


    inverter_capacity = serializers.IntegerField(
        required=False,
        allow_null=True
    )


    def validate(self, data):

        company = data.get("inverter_company")
        capacity = data.get("inverter_capacity")


        # Hybrid ke liye capacity zaroori nahi

        if company != "Hybrid" and capacity not in [8, 10]:

            raise serializers.ValidationError(
                "Capacity must be 8 or 10 for this inverter company."
            )


        # Hybrid ke case me capacity null kar do

        if company == "Hybrid":

            data["inverter_capacity"] = None


        return data