from django.urls import path
from .views import *

urlpatterns = [
    path('', TransactionsList.as_view(), name='transactions'),
    path('detail', TransactionDetail.as_view(), name='detail')
]


