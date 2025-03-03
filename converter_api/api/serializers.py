from rest_framework import serializers
from .models import ConversionHistory
from django.contrib.auth.models import User

class ConversionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversionHistory
        fields = ["id", "from_currency", "to_currency", "amount", "convert_amount", "conversion_rate", "timestamp"]
        
        
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ["username", "password", "email"]
        
    def validate(self, data):
        if User.objects.filter(username=data["username"]).exists():
            raise serializers.ValidationError("Esse username está atribuido a outro usuário.")
        return data
        
    def create(self, data):
        # Cria o usuário com a senha criptografada
        user = User.objects.create_user(
            username=data["username"],
            password=data["password"],
            email=data.get("email", "")
        )
        
        return user
    