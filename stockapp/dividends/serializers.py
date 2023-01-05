from rest_framework import serializers
from .models import Dividend


class DividendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dividend
        fields = '__all__'
        # extra_kwargs = {
        #     'portfolioId': {'write_only': True}
        # }
