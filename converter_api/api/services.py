import requests
from .crypto import convert_name
from django.core.exceptions import ValidationError
from decouple import config
from django.core.cache import cache
import json

def convert_currency_crypto(from_currency, to_currency, amount):
    # Faz a conversão das criptos
    
    # Obtém os nomes apropriados
    names = convert_name(from_currency, to_currency)
    from_currency = names["from_currency"]
    to_currency = names["to_currency"]   
     
    # Declaro as variáveis como none
    coin_origin = None
    coin_destiny = None          
    
    # Chave única do cache
    cache_key = f"{from_currency}_{to_currency}"
    # Tenta obter os dados do cache
    cache_json = cache.get(cache_key)
    # Verifica se os dados foram obtidos
    if cache_json:
        # Converte para dicionário
        cache_dict = json.loads(cache_json)
        # Tenta obter os valores do dicionário
        coin_origin = cache_dict["from_currency"]
        coin_destiny = cache_dict["to_currency"]
    
    # Verifica se os dados do cache existem
    if not coin_origin or not coin_destiny:
        # Faz a requisição get para a API externa
        response = requests.get("https://api.coingecko.com/api/v3/simple/price", params={"ids": f"{from_currency},{to_currency}", "vs_currencies": "usd"})
        
        if response.status_code == 200:
            # Transforma os dados em json
            data = response.json()
            
            # Obtém os valores das criptos em dólar
            coin_origin = data[from_currency]["usd"]
            coin_destiny = data[to_currency]["usd"]
            # Dicionário para cache
            data_cache = {"from_currency": coin_origin, "to_currency": coin_destiny}
            # Salva no cache por 1 hora
            cache.set(cache_key, json.dumps(data_cache), timeout=3600)
        
        else:
            # Retorna error
            raise ValidationError("Conversão não permitida.")
        
    # Retorna o valor da conversão e a taxa
    return {"convert_amount": f"{((float(amount) * coin_origin) / coin_destiny):.8f}", "conversion_rate": f"{(coin_origin / coin_destiny):.8f}"}
    
 
def convert_currency_coin(from_currency, to_currency, amount):
    # Faz a conversão das moedas
    
    # Verifica se o amount é válido
    if float(amount) < 0.01:
        # Retorna error
        raise ValidationError("Valor da moeda inválido.")
    else:
        # Chave única do cache
        cache_key = f"{from_currency}_{to_currency}"
        # Tenta pegar do cache
        conversion_rate = cache.get(cache_key)
        # Verifica se conseguiu pegar do cache a taxa
        if not conversion_rate:
            # Chave da API externa
            API_KEY = config("API_KEY")
            # url
            url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{from_currency}/{to_currency}"
            # Faz a requisição get pra api externa
            response = requests.get(url)
            # Verifica se o status foi 200
            if response.status_code == 200:
                # Transforma a resposta da api em json
                data = response.json()
                # Obtém a taxa de conversão
                conversion_rate = data["conversion_rate"]
                # Salva no cache por 1 hora
                cache.set(cache_key, conversion_rate, timeout=3600)
             
        # Verifca se a taxa existe
        if conversion_rate:
            # Retorna o valor da conversão e a taxa 
            return {"convert_amount": float(amount) * conversion_rate, "conversion_rate": conversion_rate}
        else:
            # Retorna error
            raise ValidationError("Essa conversão não é permitida.")
            