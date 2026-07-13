from rest_framework import serializers


class SolarCalculatorSerializer(serializers.Serializer):

    panel_quantity = serializers.IntegerField(
        min_value=1
    )


    panel_watt = serializers.ChoiceField(
        choices=[585, 600 ,615, 665, 710]
    )


    frame_quantity = serializers.IntegerField(
        min_value=0
    )


    inverter_company = serializers.ChoiceField(
        choices=[
            "None",
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

        # None aur Hybrid ke liye capacity ki zaroorat nahi

        if company in ["None", "Hybrid"]:
            data["inverter_capacity"] = None
            return data

        # Desi aur Galaxy ke liye capacity required hai

        if capacity not in [8, 10]:
            raise serializers.ValidationError(
                "Capacity must be 8 or 10."
            )

        return data