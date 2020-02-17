from django.urls import path
from portfolio import views
from portfolio.views import StockListView, PriceListView, TransactionListView, HoldingListView, AccountListView, AccountDetailView

urlpatterns = [
    path("", views.home, name="home"),
    path("stocks/", StockListView.as_view()),
    path("prices/", PriceListView.as_view()),
    path("transactions/", TransactionListView.as_view()),
    path("holdings/", HoldingListView.as_view()),
    path("summary/", views.summary),
    path("account/", AccountListView.as_view()),
    path('account/<int:pk>', views.AccountDetailView.as_view(), name='account-detail'),
    path('transaction/new/', views.transaction_new, name='transaction_new'),
]