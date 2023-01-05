import requests as r
import pandas as pd
from transactions.models import Transaction
from dividends.models import Dividend
from stocks.models import Company


def company_data(symbol):
    url = f"https://financialmodelingprep.com/api/v3/profile/{symbol}?apikey=201bc87f43b0582116c5fbb6d9f91b09"
    data = r.get(url).json()[0]
    response = {
        'symbol': data['symbol'],
        'name': data['companyName'],
        'price': data['price'],
        'logo_url': data['image'],
        'sector': data['sector'],
        'company_desc': data['description'],
        'website': data['website'],
        'industry': data['industry'],
        'currency': data['currency'],
        'lastDiv': round(data['lastDiv'], 2),
        'exchange': data['exchangeShortName']
    }
    return response


def get_portfolio(portfolioid):
    stocks = Transaction.objects.filter(portfolioId=portfolioid)
    data = stocks.values_list('symbol', flat=True)
    return sorted(set(data))


# TODO: create functions for get all portfolio data, then particular functions for dividends


def portfolio_by(attribute, portfolio_id, values='value'):
    transactions = Transaction.objects.filter(portfolioId=portfolio_id)
    dates = []
    value = []
    stock = []
    sector = []
    estimated = []

    for transaction in transactions:
        company = Company.objects.get(symbol=transaction.symbol)
        dates.append(transaction.timestamp)
        value.append(transaction.costs())
        stock.append(transaction.symbol)
        sector.append(company.sector)
        estimated.append(round(company.lastDiv*transaction.shares, 2))

    df = pd.DataFrame(data={'date': dates, 'stock': stock, 'sector': sector, 'value': value, 'estimatedDiv': estimated})
    df['year'] = pd.DatetimeIndex(df['date']).year.astype(str)
    df['month'] = pd.to_datetime(df['date']).dt.to_period('M').astype(str)

    data = df.groupby(attribute)[values].sum()

    return data.to_dict()


def dividend_by(attribute, portfolio_id):
    dividends = Dividend.objects.filter(portfolioId=portfolio_id)
    dates = []
    value = []
    stock = []

    for dividend in dividends:
        dates.append(dividend.date)
        value.append(dividend.amount)
        stock.append(dividend.symbol)
    df = pd.DataFrame(data={'date': dates, 'stock': stock, 'value': value})
    df['year'] = pd.DatetimeIndex(df['date']).year.astype(str)
    df['month'] = pd.to_datetime(df['date']).dt.to_period('M').astype(str)

    data = df.groupby(attribute)['value'].sum()

    return data.to_dict()
