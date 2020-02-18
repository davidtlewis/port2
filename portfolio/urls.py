from django.urls import path
from portfolio import views
from portfolio.views import StockListView, PriceListView, TransactionListView, HoldingListView, AccountListView, AccountDetailView, HoldingDetailView

urlpatterns = [
    path("", views.home, name="home"),
    path("stock/", StockListView.as_view()),
    path("price/", PriceListView.as_view()),
    path("transaction/", TransactionListView.as_view()),
    path("holding/", HoldingListView.as_view()),
    path("summary/", views.summary),
    path("account/", AccountListView.as_view()),
    path('account/<int:pk>', AccountDetailView.as_view(), name='account_detail'),
    path('holding/<int:pk>', HoldingDetailView.as_view(), name='holding_detail'),
    path('transaction/<int:pk>', views.TransactionDetailView.as_view(), name='transaction_detail'),
    path('stock/<int:pk>', views.StockDetailView.as_view(), name='stock_detail'),
    path('transaction/new/', views.transaction_new, name='transaction_new'),
]