import uuid
from django.db import models
from stocks.models import Portfolio


class Transaction(models.Model):
    transactionId = models.UUIDField(default=uuid.uuid4)
    symbol = models.CharField(max_length=255)
    timestamp = models.DateField()
    price = models.DecimalField(max_digits=9, decimal_places=2)
    shares = models.DecimalField(max_digits=9, decimal_places=2)
    portfolioId = models.ForeignKey(to=Portfolio, to_field='portfolioId', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return self.symbol

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        self.symbol = self.symbol.upper()
        super(Transaction, self).save(force_insert, force_update, *args, **kwargs)

    def costs(self):
        return round(self.price * self.shares, 2)
