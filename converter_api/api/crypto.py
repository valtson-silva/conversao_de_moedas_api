from django.core.exceptions import ValidationError

# Siglas das moedas e seus respectivos nomes
symbol_to_id = {
        "BTC": "bitcoin",
        "ETH": "ethereum",
        "XRP": "ripple",
        "LTC": "litecoin",
        "ADA": "cardano",
        "DOT": "polkadot",
        "BNB": "binancecoin",
        "LINK": "chainlink",
        "SOL": "solana",
        "DOGE": "dogecoin",
        "SHIB": "shiba-inu",
        "UNI": "uniswap",
        "LUNA": "terra-luna",
        "MATIC": "matic-network"
    }

def convert_name(from_currency, to_currency):    
    # Faz a conversão das siglas pelos nomes das criptos
    
    # Verifica se as moedas são válidas
    if from_currency in symbol_to_id.keys() and to_currency in symbol_to_id.keys():
        # Itera pelas chaves do dicionário
        for symbol in symbol_to_id.keys():
            if from_currency == symbol:
                # Coloca o nome no lugar da sigla
                from_currency = symbol_to_id[symbol]
                
        # Itera pelas chaves do dicionário
        for symbol in symbol_to_id.keys():
                if to_currency == symbol:
                    # Coloca o nome no lugar da sigla
                    to_currency = symbol_to_id[symbol]
                    
        return {"from_currency": from_currency, "to_currency": to_currency}
    else:
        raise ValidationError("Essa conversão não é permitida.")
