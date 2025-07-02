from django.db import models
from decimal import Decimal


class Brand(models.Model):
    name = models.CharField(max_length=255)
    daily_budget = models.DecimalField(max_digits=10, decimal_places=2)
    monthly_budget = models.DecimalField(max_digits=10, decimal_places=2)
    daily_spend = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    monthly_spend = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    def __str__(self) -> str:
        return self.name


class Campaign(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='campaigns')
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    start_hour = models.IntegerField()  # 0-23
    end_hour = models.IntegerField()    # 0-23

    def __str__(self) -> str:
        return self.name
