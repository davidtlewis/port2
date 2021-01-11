from django.shortcuts import render
from django.urls import path, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import DetailView
from django_tables2 import SingleTableView
from django_tables2.views import SingleTableMixin
from django_filters.views import FilterView
from .models import Stock, Price, Holding, Transaction, Account, HistoricPrice, Dividend
from .tables import StockTable, HoldingTable, TransactionTable, PriceTable, AccountTable, HistoricPriceTable, DividendTable
from django.db.models import Sum
from .forms import TransactionForm, CommandForm
from django.shortcuts import redirect
from django.core import management
from django.contrib.auth.decorators import login_required
from .filters import HoldingByAccountFilter, TransactionByAccountFilter, HistoricPriceByStockFilter, DividendByStockFilter
from datetime import datetime, date
import time

def home(request):
    return HttpResponse("Hello, Django!")

class StockListView(SingleTableView):
    model = Stock
    table_class = StockTable
    template_name = 'portfolio/stock.html'

def StockVolumesView(request):
    stock_volumes = Holding.objects.values('stock__name').annotate(share_volume=Sum('volume'))
    return render(request, 'portfolio/stock_volumes.html', {'stock_volumes': stock_volumes,}, )

class PriceListView(SingleTableView):
    model = Price
    table_class = PriceTable
    template_name = 'portfolio/price.html'
    paginate_by = 10

class HoldingListViewFiltered(SingleTableMixin, FilterView):
    model = Holding
    table_class = HoldingTable
    template_name = 'portfolio/holding.html'
    filterset_class = HoldingByAccountFilter

class HistoricPriceListView(SingleTableMixin, FilterView):
    model = HistoricPrice
    table_class = HistoricPriceTable
    template_name = 'portfolio/historicprice.html'
    filterset_class = HistoricPriceByStockFilter

class DividendListView(SingleTableMixin, FilterView):
    model = Dividend
    table_class = DividendTable
    template_name = 'portfolio/dividend.html'
    filterset_class = DividendByStockFilter

class HoldingListView(SingleTableView):
    model = Holding
    table_class = HoldingTable
    template_name = 'portfolio/holding.html'

class TransactionListView(SingleTableView):
    model = Transaction
    table_class = TransactionTable
    template_name = 'portfolio/transaction.html'
    paginate_by = 10

class TransactionListViewFiltered(SingleTableMixin, FilterView):
    model = Transaction
    table_class = TransactionTable
    template_name = 'portfolio/transaction.html'
    filterset_class = TransactionByAccountFilter

class AccountListView(SingleTableView):
    model = Account
    table_class = AccountTable
    template_name = 'portfolio/account.html'

def summary(request):
    totals = Account.objects.aggregate(Sum('account_value'))
    accounts = Account.objects.all()
    #accounts_by_type = Account.objects.values('account_type').annotate(total_value=Sum('account_value'))
    a = Account.objects.filter(person__name = "david") | Account.objects.filter(person__name = "henri")
    accounts_by_type = a.values('account_type').annotate(total_value=Sum('account_value'))
    return render(request, 'portfolio/summary.html', {
    'totals': totals, 'accounts':accounts, 'accounts_by_type': accounts_by_type,
    }, )

class AccountDetailView(DetailView):
    model = Account
    template_name = 'portfolio/account_detail.html'

    """def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        holding_list = Account..objects.all()
        context['holding_list'] = holding_list
        return context
"""

class TransactionDetailView(DetailView):
    model = Transaction
    template_name = 'portfolio/transaction_detail.html'

class HoldingDetailView(DetailView):
    model = Holding
    template_name = 'portfolio/holding_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        transaction_list = Transaction.objects.filter(account=self.object.account).filter(stock=self.object.stock)
        #transaction_list = Transaction.objects.filter(stock=self.stock)
        #transaction_list = Transaction.objects.all()
        context['transaction_list'] = transaction_list
        return context

class StockDetailView(DetailView):
    model = Stock
    template_name = 'portfolio/stock_detail.html'

def transaction_new(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            #transaction.account = request.account
            #transaction.transaction_type = request.transaction_type
            #transaction.date = request.date
            #transaction.stock = request.stock
            #transaction.volume = request.volume
            #transaction.tcost = request.tcost
            transaction.save()
            return redirect('transaction_detail', pk=transaction.pk)
    else:
        form = TransactionForm()
    return render(request, 'portfolio/transaction_edit.html', {'form': form})


"""class CommandView(TemplateView):
    template_name = "portfolio/commands.html"

    def get(self,request):
        form = CommandForm()
        return render(request, self.template_name, {'form':form})
"""
@login_required
def command(request):
    if request.method =='POST':
        form = CommandForm(request.POST)
        if form.is_valid():
            do_get_prices = form.cleaned_data['do_get_prices']
            do_refresh_accounts = form.cleaned_data['do_refresh_accounts']
            do_refresh_holdings = form.cleaned_data['do_refresh_holdings']
            do_get_history = form.cleaned_data['do_get_history']
            do_get_perf = form.cleaned_data['do_get_perf']

            if do_get_prices:
                management.call_command('get_prices')
            if do_refresh_accounts:
                management.call_command('refresh_accounts')
            if do_refresh_holdings:
                management.call_command('refresh_holdings')
            if do_get_perf:
                management.call_command('get_perf')
            if do_get_history:
                stocks = Stock.objects.all()
                today = date.today()
                for stock in stocks:
                    stock.get_historic_prices()

        return HttpResponseRedirect(reverse('index') )
    else:
        form = CommandForm()
        context = {
            'form': form
        }
    return render(request, 'portfolio/commands.html', context)