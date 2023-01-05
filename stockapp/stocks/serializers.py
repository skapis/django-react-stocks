from rest_framework import serializers
from .models import Company, Portfolio


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class PortfolioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Portfolio
        fields = '__all__'
        extra_kwargs = {
            'owner': {'write_only': True}
        }
