from django.urls import path
from .views import RefreshAccountsView, RefreshPricesView, PriceRefreshProgressView

urlpatterns = [
    path('refresh-accounts/', RefreshAccountsView.as_view(),
         name='refresh-accounts'),
    path('refresh-prices/', RefreshPricesView.as_view(), name='refresh-prices'),
    path('price-refresh-progress/', PriceRefreshProgressView.as_view(),
         name='price-refresh-progress'),
]
