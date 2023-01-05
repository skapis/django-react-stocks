from django.shortcuts import render
from .models import Dividend
from .serializers import DividendSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from stocks.models import Portfolio, Company
from stocks.functions import get_portfolio
from transactions.models import Transaction


class DividendList(APIView):
    def get(self, request):
        portfolio_id = request.GET.get('portfolioId', None)
        if portfolio_id:
            portfolio = Portfolio.objects.get(portfolioId=portfolio_id)
            div_records = Dividend.objects.filter(portfolioId=portfolio.pk)
            serializer = DividendSerializer(div_records, many=True)
            stocks = get_portfolio(portfolio_id)

            portfolio_value = 0
            current_value = 0
            acq_div = 0
            est_div = 0

            for stock in stocks:
                company = Company.objects.get(symbol=stock)
                transactions = Transaction.objects.filter(symbol=stock, portfolioId=portfolio_id)
                dividends = Dividend.objects.filter(symbol=stock, portfolioId=portfolio_id)
                shares = 0
                total_value = 0
                market_value = 0
                acq_dividends = 0
                est_dividends = 0

                for transaction in transactions:
                    shares += transaction.shares
                    total_value += transaction.costs()
                    market_value += transaction.shares * company.price

                for dividend in dividends:
                    acq_dividends += dividend.amount

                est_dividends += shares * company.lastDiv

                portfolio_value += total_value
                current_value += market_value
                acq_div += acq_dividends
                est_div += est_dividends

            if portfolio_value != 0:
                response = {
                    'total': acq_div,
                    'divYieldInvest': round(est_div/portfolio_value, 2) * 100,
                    'divYieldMarket': round(est_div/current_value, 2) * 100,
                    'estDividend': est_div,
                    'items': serializer.data
                }
            else:
                response = {
                    'total': 0,
                    'divYieldInvest': 0,
                    'divYieldMarket': 0,
                    'estDividend': 0,
                    'items': []
                }
            return Response(response, status=status.HTTP_200_OK)

        return Response({'error': 'portfolioId is required'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        data = request.data
        serializer = DividendSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DividendDetail(APIView):
    def get_dividend(self, id):
        return Dividend.objects.get(dividendId=id)

    def get(self, request):
        dividend_id = request.GET.get('dividendId', None)
        if dividend_id:
            dividend = self.get_dividend(dividend_id)
            serializer = DividendSerializer(dividend)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error': 'dividendId is required'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        data = request.data
        dividend_id = request.GET.get('dividendId', None)
        if dividend_id:
            dividend = self.get_dividend(dividend_id)
            serializer = DividendSerializer(dividend, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'dividendId is required'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        dividend_id = request.GET.get('dividendId', None)
        if dividend_id:
            dividend = self.get_dividend(dividend_id)
            dividend.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'error': 'dividendId is required'}, status=status.HTTP_404_NOT_FOUND)



