from django.urls import path
from .views import *

urlpatterns = [
    path('', CompanyList.as_view(), name='companies'),
    path('portfolio', UserPortfolio.as_view(), name='portfolio'),
    path('stock', CompanyDetailUser.as_view(), name='holdingDetail'),
    path('detail', CompanyDetail.as_view(), name='detail'),
    path('portfoliodata', PortfolioBy.as_view(), name='portfolio_data'),
    path('dividenddata', DividendBy.as_view(), name='dividend_data')
]
