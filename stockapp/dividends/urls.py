from django.urls import path
from .views import *

urlpatterns = [
    path('', DividendList.as_view(), name='dividends'),
    path('detail', DividendDetail.as_view(), name='dividend_detail')
]