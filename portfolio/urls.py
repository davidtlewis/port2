from django.urls import path
from portfolio import views
from portfolio.views import StockListView, PriceListView, TransactionListView, HoldingListView

urlpatterns = [
    path("", views.home, name="home"),
    path("stocks/", StockListView.as_view()),
    path("prices/", PriceListView.as_view()),
    path("transactions/", TransactionListView.as_view()),
    path("holdings/", HoldingListView.as_view()),
    path("summary/", views.summary),
]