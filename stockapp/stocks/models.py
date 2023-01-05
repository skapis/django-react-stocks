import uuid
from django.db import models
from django.utils.timezone import now
from userprofile.models import Profile


class Company(models.Model):
    company_id = models.UUIDField(default=uuid.uuid4)
    symbol = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    logo_url = models.CharField(max_length=255, default='none')
    sector = models.CharField(max_length=255, default='none')
    company_desc = models.TextField()
    website = models.CharField(max_length=255)
    industry = models.CharField(max_length=255)
    currency = models.CharField(max_length=255)
    lastDiv = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    exchange = models.CharField(max_length=255)
    updated_at = models.DateTimeField(default=now)

    class Meta:
        verbose_name_plural = 'Companies'

    def __str__(self):
        return self.name


class Portfolio(models.Model):
    profile = models.ForeignKey(to=Profile, to_field='profileId', on_delete=models.CASCADE)
    portfolioId = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=255)
    currency = models.CharField(max_length=255, default='USD')

    def __str__(self):
        return self.name
