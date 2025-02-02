from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .services import convert_currency_crypto, convert_currency_coin
from .serializers import ConversionHistorySerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache
from .models import ConversionHistory
import json

class ConversionCryptoView(APIView):
    # Registra a conversão de cripto no banco de dados
    
    # Verifica se o usuário está autenticado
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # Obtém a moeda origem
        from_currency = request.data["from_currency"]
        # Obtém a moeda destino
        to_currency = request.data["to_currency"]
        # Obtém o valor
        amount = request.data["amount"]
        # Faz a conversão
        conversion = convert_currency_crypto(from_currency, to_currency, amount)
        # Faz o dicionário com as informações obtidas
        data = {
            "from_currency": from_currency,
            "to_currency": to_currency,
            "amount": amount,
            "convert_amount": float(conversion["convert_amount"]),
            "conversion_rate": float(conversion["conversion_rate"])
        }
        
        # Serializa os dados
        serializer = ConversionHistorySerializer(data=data)
        # Verifica se os dados são válidos
        if serializer.is_valid():
            # Salva a conversão no banco de dados
            serializer.save()
            
            # Deleta o cache antigo 
            cache.delete("conversion_list")
            # Salva o cache atualizado
            conversions = ConversionHistory.objects.all()
            cache_serializer = ConversionHistorySerializer(conversions, many=True)
            cache.set("conversion_list", json.dumps(cache_serializer.data), timeout=60*300)
            
            # Retorna a conversão e o status 201
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # Retorna error e o status 400
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class ConversionCoinView(APIView):
    # Registra a conversão de moedas tradicionais no banco de dados
    
    # Verifica se o usuário está autenticado
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # Obtém a moeda origem
        from_currency = request.data["from_currency"]
        # Obtém a moeda destino
        to_currency = request.data["to_currency"]
        # Obtém o valor
        amount = request.data["amount"]
        # Faz a conversão
        conversion = convert_currency_coin(from_currency, to_currency, amount)
        
        # Faz o dicionário com as informações obtidas
        data = {
            "from_currency": from_currency,
            "to_currency": to_currency,
            "amount": amount,
            "convert_amount": conversion["convert_amount"],
            "conversion_rate": conversion["conversion_rate"]
        }
        
        # Serializa os dados
        serializer = ConversionHistorySerializer(data=data)
        # Verifica se os dados são válidos
        if serializer.is_valid():
            # Salva a conversão no banco de dados
            serializer.save()
            
            # Deleta o cache antigo 
            cache.delete("conversion_list")
            # Salva o cache atualizado
            conversions = ConversionHistory.objects.all()
            cache_serializer = ConversionHistorySerializer(conversions, many=True)
            cache.set("conversion_list", json.dumps(cache_serializer.data), timeout=60*300)
            
             # Retorna a conversão e o status 201
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # Retorna error e o status 400
            return Response({"error": "Dados informados inválidos."}, status=status.HTTP_400_BAD_REQUEST)
        
class RegisterUserView(APIView):
    # Registra um usuário
    
    def post(self, request):
        # Serializa o dados recebidos no corpo da requisição
        serializer = UserSerializer(data=request.data)
        # Verifica se os dados são válidos
        if serializer.is_valid():
            # Salva o usuário no banco de dados
            serializer.save()
            
            # Retorna o usuário criado e o status 201
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # Retorna error e o status 400
            return Response({"error": "Dados inválidos"}, status=status.HTTP_400_BAD_REQUEST)
        
class ConversionListView(APIView):
    # Mostra todas as conversões feitas
    
    # Verifica se o usuário está autenticado
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Tenta obter o todas as conversões
        cache_list = cache.get("conversion_list")
        
        # Verifica se o cache existe
        if not cache_list:
            # Obtém todas as conversões
            conversions = ConversionHistory.objects.all()
            # Serializa todas as conversões
            serializer = ConversionHistorySerializer(conversions, many=True)
            
            # Salva todas as conversões no cache por 5 horas
            cache.set("conversion_list", json.dumps(serializer.data), timeout=60*300)
            
            # Retorna as conversões e o status 200
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # Retorna as conversões e o status 200
            return Response(json.loads(cache_list), status=status.HTTP_200_OK)
        