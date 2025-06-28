from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth import get_user_model


User = get_user_model()


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = User.EMAIL_FIELD 

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError("Email ou senha inválidos")

        if not user.is_active:
            raise serializers.ValidationError("Conta inativa.")

        data = super().validate(attrs)
        return data
        
        
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ["email", "password"]
        
    def validate(self, data):
        if User.objects.filter(email=data["email"]).exists():
            raise serializers.ValidationError("Esse email já está atribuido a outro usuário.")
        return data
        
    def create(self, data):
        user = User.objects.create_user(
            password=data["password"],
            email=data["email"]
        )
        
        return user
    