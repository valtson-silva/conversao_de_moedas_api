from django.db import models
from django.core.exceptions import ValidationError

# Cria o modelo de histórico de conversões
class ConversionHistory(models.Model):
    from_currency = models.CharField(max_length=10, null=False)
    to_currency = models.CharField(max_length=10, null=False)
    amount = models.DecimalField(max_digits=20, decimal_places=8, null=False)
    convert_amount = models.DecimalField(max_digits=20, decimal_places=8, null=False)
    conversion_rate = models.DecimalField(max_digits=20, decimal_places=8, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Lista de todas as moedas permitidas
    valid_currencies = [
            "USD", "BRL", "BTC", "ETH", "EUR", "JPY", "XRP", "LTC", "ADA", 
            "DOT", "BNB", "LINK", "SOL", "DOGE", "SHIB", "UNI", "LUNA", 
            "MATIC", "GBP", "CNY", "AUD", "CAD", "CHF", "INR"
        ]
    
    def clean(self):
        # Verifica se a moeda de origem é válida
        if self.from_currency not in self.valid_currencies:
            raise ValidationError(f"Moeda de origem '{self.from_currency}' não é válida.")
        
        # Verifica se a moeda de destino é válida
        if self.to_currency not in self.valid_currencies:
            raise ValidationError(f"Moeda de destino '{self.to_currency}' não é válida.")
        
        # Verifica se as moedas de destino e origem são iguais
        if self.to_currency == self.from_currency:
            raise ValidationError(f"Moeda de destino e moeda de origem precisam ser diferentes.")
        
    def save(self, *args, **kwargs):
        # Chama a validação antes de salvar
        self.clean()
        
        super().save(*args, **kwargs)
