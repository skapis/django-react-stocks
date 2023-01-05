from django.urls import path
from .views import *

urlpatterns = [
    path('currentprice', CurrentPrice.as_view(), name='currentPrice'),
    path('csrf', GetCSRFToken.as_view(), name='csrf')
]
