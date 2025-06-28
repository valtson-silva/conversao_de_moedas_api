import json
from django.core.exceptions import ValidationError
from django.core.cache import cache

from .coversion_services import convert_currency_crypto, convert_currency_coin
from .serializers import ConversionHistorySerializer
from .models import ConversionHistory


def conversion_crypto(data):
    try:
        from_currency = data["from_currency"]
        to_currency = data["to_currency"]
        amount = data["amount"]

        conversion = convert_currency_crypto(from_currency, to_currency, amount)
    except ValidationError as e:
        raise ValidationError(f"{e}")
    
    data_dict = {
        "from_currency": from_currency,
        "to_currency": to_currency,
        "amount": amount,
        "convert_amount": float(conversion["convert_amount"]),
        "conversion_rate": float(conversion["conversion_rate"])
    }
    
    serializer = serializer_data(data_dict)
    cache_set()

    return serializer


def conversion_coin(data):
    try:
        from_currency = data["from_currency"]
        to_currency = data["to_currency"]
        amount = data["amount"]

        conversion = convert_currency_coin(from_currency, to_currency, amount)
    except ValidationError as e:
        raise ValidationError(f"{e}")
    
    data_dict = {
        "from_currency": from_currency,
        "to_currency": to_currency,
        "amount": amount,
        "convert_amount": conversion["convert_amount"],
        "conversion_rate": conversion["conversion_rate"]
    }
    
    serializer = serializer_data(data_dict)
    cache_set()

    return serializer


def cache_set():
    conversions = ConversionHistory.objects.all()
    cache_serializer = ConversionHistorySerializer(conversions, many=True)
    cache.set("conversion_list", json.dumps(cache_serializer.data), timeout=60*5)


def serializer_data(data):
    try:
        serializer = ConversionHistorySerializer(data=data)
        serializer.is_valid(raise_exception=True)
    except ValidationError as e:
        raise ValidationError(f"{e}")
    
    serializer.save()
    return serializer.data


def conversion_list():
    cached_data = cache.get("conversion_list")
    
    if not cached_data:
        conversions = ConversionHistory.objects.all()
        serializer = ConversionHistorySerializer(conversions, many=True)
        return serializer.data
    
    return json.loads(cached_data)
    

def conversion_delete(conversion_id):
    try:
        conversion = ConversionHistory.objects.get(id=conversion_id)
    except ValidationError as e:
        raise ValidationError(f"{e.detail}")
    
    conversion.delete()
    cache.delete("conversion_list")
    return "Conversão deletada com sucesso"
