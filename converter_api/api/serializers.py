from rest_framework import serializers

from .models import ConversionHistory


class ConversionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversionHistory
        fields = ["id", "from_currency", "to_currency", "amount", "convert_amount", "conversion_rate", "timestamp"]
        