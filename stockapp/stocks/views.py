from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .functions import get_portfolio, portfolio_by, company_data, dividend_by
from .models import Company, Portfolio
from .serializers import CompanySerializer, PortfolioSerializer
from transactions.models import Transaction
from transactions.serializers import TransactionSerializer
from dividends.models import Dividend
from dividends.serializers import DividendSerializer


class CompanyList(APIView):
    def get(self, request):
        companies = Company.objects.all()
        serializer = CompanySerializer(companies, many=True)
        response = {
            'total': companies.count(),
            'items': serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data

        symbol = request.data['symbol'].upper()
        company = Company.objects.filter(symbol=symbol)
        tserializer = TransactionSerializer(data=data)

        if company.exists():
            if tserializer.is_valid():
                tserializer.save()
                return Response(tserializer.data, status=status.HTTP_200_OK)
            return Response(tserializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            cdata = company_data(data['symbol'])
            cserializer = CompanySerializer(data=cdata)
            if cserializer.is_valid():
                cserializer.save()
                if tserializer.is_valid():
                    tserializer.save()
                    return Response(tserializer.data, status=status.HTTP_200_OK)
                return Response(tserializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(cserializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CompanyDetail(APIView):
    def get(self, request):
        symbol = request.GET.get('symbol', None)
        if symbol:
            try:
                company = Company.objects.get(symbol=symbol)
                serializer = CompanySerializer(company)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except:
                return Response({'result': 'not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'error': 'symbol is required'}, status=status.HTTP_400_BAD_REQUEST)


class UserPortfolio(APIView):
    def transaction_sum(self, portfolioid):
        agg_data = []
        stocks = get_portfolio(portfolioid)
        portfolio_value = 0
        current_value = 0
        acq_div = 0
        est_div = 0

        for stock in stocks:
            company = Company.objects.get(symbol=stock)
            transactions = Transaction.objects.filter(symbol=stock, portfolioId=portfolioid)
            dividends = Dividend.objects.filter(symbol=stock, portfolioId=portfolioid)
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

            data = {
                'symbol': company.symbol,
                'shares': shares,
                'totalValue': round(total_value, 2),
                'marketValue': round(market_value, 2),
                'gainLoss': round(market_value - total_value, 2),
                'glPrc': round(((market_value - total_value) / total_value), 2),
                'acqDividends': acq_dividends,
                'estDividends': round(est_dividends, 2)
            }
            portfolio_value += total_value
            current_value += market_value
            acq_div += acq_dividends
            est_div += est_dividends
            agg_data.append(data)

        return agg_data, portfolio_value, current_value, acq_div, est_div

    def get(self, request):
        portfolioid = request.GET.get('portfolioId', None)
        if portfolioid:
            portfolio = Portfolio.objects.get(portfolioId=portfolioid)
            serializer = PortfolioSerializer(portfolio)
            data = self.transaction_sum(portfolio.pk)
            companies = data[0]
            total_value = data[1]
            current_value = data[2]
            acq_div = data[3]
            est_div = data[4]
            gain_loss = current_value - total_value
            try:
                gl_prc = round(((current_value - total_value) / total_value), 2)
            except:
                gl_prc = 0

            response = {
                'portfolio': serializer.data,
                'total': len(data[0]),
                'totalValue': total_value,
                'currentValue': current_value,
                'gainLoss': gain_loss,
                'gainLossPrc': gl_prc,
                'acqDividends': acq_div,
                'estDividends': est_div,
                'data': companies
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response({'error': 'portfolioId is required'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        data = request.data
        serializer = PortfolioSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        portfolio_id = request.GET.get('portfolioId', None)
        if portfolio_id:
            if portfolio_id:
                portfolio = Portfolio.objects.get(portfolioId=portfolio_id)
                serializer = PortfolioSerializer(portfolio, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'portfolioId is required'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        portfolio_id = request.GET.get('portfolioId', None)
        if portfolio_id:
            portfolio = Portfolio.objects.get(portfolioId=portfolio_id)
            portfolio.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'error': 'portfolioId is required'}, status=status.HTTP_404_NOT_FOUND)


class CompanyDetailUser(APIView):
    def company_data(self, symbol, portfolio):
        company = Company.objects.get(symbol=symbol)
        transactions = Transaction.objects.filter(symbol=symbol, portfolioId=portfolio)
        dividends = Dividend.objects.filter(symbol=symbol, portfolioId=portfolio)
        total_value = 0
        market_value = 0
        shares = 0
        acq_dividend = 0
        for transaction in transactions:
            total_value += transaction.costs()
            shares += transaction.shares
            market_value += transaction.shares * company.price

        for dividend in dividends:
            acq_dividend += dividend.amount

        holding = {
            'total_value': total_value,
            'market_value': round(market_value, 2),
            'shares': shares,
            'gainLoss': market_value - total_value,
            'glPrc': round(((market_value - total_value) / total_value), 2)*100,
            'estDividend': round(company.lastDiv * shares, 2),
            'acqDividend': acq_dividend
        }

        return company, transactions, holding, dividends

    def get(self, request):
        portfolioid = request.GET.get('portfolioId', None)
        if portfolioid:
            portfolio = Portfolio.objects.get(portfolioId=portfolioid)
            company = request.GET.get('symbol', None)
            if Transaction.objects.filter(portfolioId=portfolio.pk, symbol=company).count() != 0:
                data = self.company_data(company, portfolio.pk)
                company_data = data[0]
                transactions = data[1]
                holding = data[2]
                dividends = data[3]

                cserializer = CompanySerializer(company_data)
                tserializer = TransactionSerializer(transactions, many=True)
                dserializer = DividendSerializer(dividends, many=True)
                response = {
                    'company': cserializer.data,
                    'holdings': holding,
                    'transactions': tserializer.data,
                    'dividends': dserializer.data
                }
                return Response(response, status=status.HTTP_200_OK)
            return Response({'error': 'This company is not in selected portfolio'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'error': 'portfolioId is required'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        symbol = request.GET.get('symbol', None)
        portfolioid = request.GET.get('portfolioId', None)
        if portfolioid and symbol:
            portfolio = Portfolio.objects.get(portfolioId=portfolioid)
            transactions = Transaction.objects.filter(symbol=symbol, portfolioId=portfolio.pk)
            transactions.delete()
            dividends = Dividend.objects.filter(symbol=symbol, portfolioId=portfolio.pk)
            dividends.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'error': 'portfolioId and symbol is required'}, status=status.HTTP_404_NOT_FOUND)


class PortfolioBy(APIView):
    def get(self, request):
        attribute = request.GET.get('by', None)
        portfolio_id = request.GET.get('portfolioId', None)
        est_div = request.GET.get('estDiv', None)

        if attribute and portfolio_id:
            if est_div == "1":
                data = portfolio_by(attribute, portfolio_id, values='estimatedDiv')
            else:
                data = portfolio_by(attribute, portfolio_id)

            response = {
                "data": data
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response({'error': 'by and portfolioId is required'}, status=status.HTTP_400_BAD_REQUEST)


class DividendBy(APIView):
    def get(self, request):
        attribute = request.GET.get('by', None)
        portfolio_id = request.GET.get('portfolioId', None)

        if attribute and portfolio_id:
            data = dividend_by(attribute, portfolio_id)

            response = {
                "data": data
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response({'error': 'by and portfolioId is required'}, status=status.HTTP_400_BAD_REQUEST)

