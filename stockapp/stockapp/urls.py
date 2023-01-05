from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('admin/', admin.site.urls),
    path('profile/', include('userprofile.urls')),
    path('transactions/', include('transactions.urls')),
    path('stocks/', include('stocks.urls')),
    path('dividends/', include('dividends.urls')),
    path('api/', include('api_data.urls'))
]

urlpatterns += [re_path(r"^.*", TemplateView.as_view(template_name='index.html'))]
