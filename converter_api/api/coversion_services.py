import requests
from django.core.exceptions import ValidationError
from decouple import config
from django.core.cache import cache
import json

from .crypto import convert_name


def conversion_rate_coin_api(from_currency, to_currency):
    """Obtém a taxa de conversão entre duas moedas"""

    API_KEY = config("API_KEY")
    
    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{from_currency}/{to_currency}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        conversion_rate = data["conversion_rate"]
        return conversion_rate
    
    
def quotation_crypto(from_currency, to_currency, cache_key):
    """Obtém a taxa de conversão entre duas criptos"""
    
    response = requests.get("https://api.coingecko.com/api/v3/simple/price", params={"ids": f"{from_currency},{to_currency}", "vs_currencies": "usd"})
        
    if response.status_code == 200:
        data = response.json()
        
        coin_origin = data[from_currency]["usd"]
        coin_destiny = data[to_currency]["usd"]
        
        data_cache = {"from_currency": coin_origin, "to_currency": coin_destiny}
        cache.set(cache_key, json.dumps(data_cache), timeout=3600)
            
        return {"from_currency": coin_origin, "to_currency": coin_destiny}
    else:
        raise ValidationError("Erro ao obter a taxa de conversão entre as moedas.")


def convert_currency_crypto(from_currency, to_currency, amount):
    """Faz a conversão das criptos"""
    
    if not type(amount).__name__ in ["int", "float"]:
        raise ValidationError("Valor da cripto inválido.")
    
    if float(amount) < 0:
        raise ValidationError("Valor da cripto inválido.")
    
    names = convert_name(from_currency, to_currency)
    from_currency = names["from_currency"]
    to_currency = names["to_currency"]   
     
    coin_origin = None
    coin_destiny = None          
    
    cache_key = f"{from_currency}_{to_currency}"
    cache_json = cache.get(cache_key)
    
    if cache_json:
        cache_dict = json.loads(cache_json)
        coin_origin = cache_dict["from_currency"]
        coin_destiny = cache_dict["to_currency"]
    
    if not coin_origin or not coin_destiny:
        data = quotation_crypto(from_currency, to_currency, cache_key)
        coin_origin = data["from_currency"]
        coin_destiny = data["to_currency"]

    return {"convert_amount": f"{((float(amount) * coin_origin) / coin_destiny):.8f}", "conversion_rate": f"{(coin_origin / coin_destiny):.8f}"}
    
 
def convert_currency_coin(from_currency, to_currency, amount):
    """Faz a conversão das moedas"""
    
    if not type(amount).__name__ in ["int", "float"]:
        raise ValidationError("Valor da moeda inválido.")
    
    if float(amount) < 0.01:
        raise ValidationError("Valor da moeda inválido.")
    
    cache_key = f"{from_currency}_{to_currency}"
    conversion_rate = cache.get(cache_key)
    
    if not conversion_rate:
        conversion_rate = conversion_rate_coin_api(from_currency, to_currency)
        cache.set(cache_key, conversion_rate, timeout=3600)
             
        if conversion_rate:
            return {"convert_amount": float(amount) * conversion_rate, "conversion_rate": conversion_rate}
        else:
            raise ValidationError("Essa conversão não é permitida.")
    
    return {"convert_amount": float(amount) * conversion_rate, "conversion_rate": conversion_rate}
            