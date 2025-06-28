from rest_framework import status
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from rest_framework.views import APIView

from .api_services import conversion_coin, conversion_crypto, conversion_delete, conversion_list


class ConversionCryptoView(APIView):
    """Faz a conversão de cripto"""
    
    def post(self, request):
        try:
            data = conversion_crypto(request.data)
        except ValidationError as e:
            return Response({"success": False, "message": e}, status=status.HTTP_400_BAD_REQUEST)           

        return Response(data, status=status.HTTP_201_CREATED)
        
        
class ConversionCoinView(APIView):
    """Faz a conversão de moedas tradicionais"""
    
    def post(self, request):
        try:
            data = conversion_coin(request.data)
        except ValidationError as e:
            return Response({"success": False, "message": e}, status=status.HTTP_400_BAD_REQUEST)           

        return Response(data, status=status.HTTP_201_CREATED)
        
        
class ConversionListView(APIView):
    """Mostra todas as conversões feitas"""
    
    def get(self, request):
        conversions = conversion_list()
        return Response(conversions, status=status.HTTP_200_OK)
        
    
class ConversionDeleteView(APIView):
    """Deleta uma conversão do banco de dados"""
    
    def delete(self, request, id):
        try:
            message = conversion_delete(id)
        except ValidationError as e:
            return Response({"success": False, "message": e}, status=status.HTTP_404_NOT_FOUND)
        
        return Response({"success": True, "message": message}, status=status.HTTP_204_NO_CONTENT)
        
