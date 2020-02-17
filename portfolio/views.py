from django.shortcuts import render
from django.urls import path
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from .models import Stock, Price, Holding, Transaction, Account
from django_tables2 import SingleTableView
from .tables import StockTable, HoldingTable, TransactionTable, PriceTable
from django.db.models import Sum
from .forms import TransactionForm

def home(request):
    return HttpResponse("Hello, Django!")

class StockListView(SingleTableView):
    model = Stock
    table_class = StockTable
    template_name = 'portfolio/stocks.html'

class PriceListView(SingleTableView):
    model = Price
    table_class = PriceTable
    template_name = 'portfolio/prices.html'

class HoldingListView(SingleTableView):
    model = Holding
    table_class = HoldingTable
    template_name = 'portfolio/holdings.html'

class TransactionListView(SingleTableView):
    model = Transaction
    table_class = TransactionTable
    template_name = 'portfolio/transactions.html'

def summary(request):
    totals = Account.objects.aggregate(Sum('account_value'))
    accounts = Account.objects.all()
    return render(request, 'portfolio/summary.html', {
    'totals': totals, 'accounts':accounts,
    }, )

class AccountListView(ListView):
    model = Account
    template_name = 'portfolio/accounts.html'

class AccountDetailView(DetailView):
    model = Account
    template_name = 'portfolio/account_detail.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        #transaction_list = Transaction.objects.all() 
        transaction_list = Transaction.objects.filter(account__id=self.object.id)
        context['transaction_list'] = transaction_list
        return context

def transaction_new(request):
    form = TransactionForm()
    return render(request, 'portfolio/transaction_edit.html', {'form': form})