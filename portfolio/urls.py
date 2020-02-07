from django.urls import path
from portfolio import views
from portfolio.views import StockListView, PriceListView

urlpatterns = [
    path("", views.home, name="home"),
    path("stock_list/", StockListView.as_view()),
    path("price_list/", PriceListView.as_view()),
]