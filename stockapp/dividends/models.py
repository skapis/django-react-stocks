import uuid
from django.db import models
from stocks.models import Portfolio


class Dividend(models.Model):
    dividendId = models.UUIDField(default=uuid.uuid4)
    symbol = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    date = models.DateField()
    portfolioId = models.ForeignKey(to=Portfolio, to_field='portfolioId', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.symbol

