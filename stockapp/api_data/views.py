import requests as r
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.middleware.csrf import get_token


class CurrentPrice(APIView):
    def get(self, request):
        symbol = request.GET.get("symbol", None)
        url = f"https://financialmodelingprep.com/api/v3/profile/{symbol}?apikey=201bc87f43b0582116c5fbb6d9f91b09"
        data = r.get(url).json()
        current_price = data[0]["price"]
        response = {
            "symbol": symbol,
            "price": current_price
        }

        return Response(data=response, status=status.HTTP_200_OK)


class GetCSRFToken(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request):
        return Response({'csrfToken': get_token(request)})
