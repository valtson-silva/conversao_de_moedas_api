from django.db import models
from django.core.exceptions import ValidationError


class ConversionHistory(models.Model):
    from_currency = models.CharField(max_length=10, null=False)
    to_currency = models.CharField(max_length=10, null=False)
    amount = models.DecimalField(max_digits=20, decimal_places=8, null=False)
    convert_amount = models.DecimalField(max_digits=20, decimal_places=8, null=False)
    conversion_rate = models.DecimalField(max_digits=20, decimal_places=8, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    
    valid_currencies = [
            "USD", "BRL", "BTC", "ETH", "EUR", "JPY", "XRP", "LTC", "ADA", 
            "DOT", "BNB", "LINK", "SOL", "DOGE", "SHIB", "UNI", "LUNA", 
            "MATIC", "GBP", "CNY", "AUD", "CAD", "CHF", "INR"
        ]
    
    
    def clean(self):
        if self.from_currency not in self.valid_currencies:
            raise ValidationError(f"Moeda de origem '{self.from_currency}' não é válida.")
        
        if self.to_currency not in self.valid_currencies:
            raise ValidationError(f"Moeda de destino '{self.to_currency}' não é válida.")
        
        if self.to_currency == self.from_currency:
            raise ValidationError(f"Moeda de destino e moeda de origem precisam ser diferentes.")
        
        
    def save(self, *args, **kwargs):
        self.clean()
        
        super().save(*args, **kwargs)
        
    
    class Meta:
        verbose_name = "Histórico de Conversão"
        verbose_name_plural = "Históricos de Conversão"
        ordering = ['-timestamp']
    
    
    def __str__(self):
        return f"{self.from_currency} para {self.to_currency}"
