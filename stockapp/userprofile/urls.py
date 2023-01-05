from django.urls import path
from .views import *

urlpatterns = [
    path('', UserProfile.as_view(), name='profile')
]
