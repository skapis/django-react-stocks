from django.shortcuts import render
from .models import Transaction
from .serializers import TransactionSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from stocks.models import Company, Portfolio


class TransactionsList(APIView):
    def get(self, request):
        portfolio_id = request.GET.get('portfolioId', None)
        if portfolio_id:
            transactions = Transaction.objects.filter(portfolioId=portfolio_id)
            serializer = TransactionSerializer(transactions, many=True)
            return Response({
                'transactions': {
                    'total': transactions.count(),
                    'items': serializer.data
                }
            }, status=status.HTTP_200_OK)
        return Response({'error': 'portfolioId is required'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        data = request.data
        serializer = TransactionSerializer(data=data)
        company = Company.objects.filter(symbol=data['symbol'])

        if serializer.is_valid() and company.exists():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransactionDetail(APIView):
    def get_transaction(self, id):
        return Transaction.objects.get(transactionId=id)

    def get(self, request):
        transaction_id = request.GET.get('transactionId', None)
        if transaction_id:
            transaction = self.get_transaction(transaction_id)
            serializer = TransactionSerializer(transaction)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error': 'transactionId is required'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        transaction_id = request.GET.get('transactionId', None)
        if transaction_id:
            transaction = self.get_transaction(transaction_id)
            data = request.data
            serializer = TransactionSerializer(transaction, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'transactionId is required'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        transaction_id = request.GET.get('transactionId', None)
        if transaction_id:
            transaction = self.get_transaction(transaction_id)
            transaction.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'error': 'transactionId is required'}, status=status.HTTP_404_NOT_FOUND)


