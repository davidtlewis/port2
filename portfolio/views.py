from django.shortcuts import render
from django.urls import path, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import DetailView
from django_tables2 import SingleTableView
from django_tables2.views import SingleTableMixin
from django_tables2.export.views import ExportMixin
from django_filters.views import FilterView
from .models import Stock, Price, Holding, Transaction, Account, HistoricPrice, Dividend
from .tables import StockTable, HoldingTable, TransactionTable, PriceTable, AccountTable, HistoricPriceTable, DividendTable, StockHoldingTable, StockListTable
from django.db.models import Sum
from .forms import TransactionForm, CommandForm
from django.shortcuts import redirect
from django.core import management
from django.contrib.auth.decorators import login_required
from .filters import HoldingByAccountFilter, HoldingByAccountFilter2, TransactionFilter, HistoricPriceByStockFilter, DividendByStockFilter
from datetime import datetime, date
import time
from django_tables2 import RequestConfig

def home(request):
    return HttpResponse("Hello, Django!")

class StockListView(SingleTableView):
    model = Stock
    table_class = StockTable
    template_name = 'portfolio/stock.html'

def StockVolumesView(request):
    stock_volumes = Holding.objects.values('stock__name').annotate(share_volume=Sum('volume'))
    return render(request, 'portfolio/stock_volumes.html', {'stock_volumes': stock_volumes,}, )

def StockHoldingView(request):
    table = StockHoldingTable(Stock.objects.annotate(sum_value=Sum('holding__current_value')))
    return render(request, "portfolio/stock_holding_summary2.html",{"table":table})

class StockHoldingView2(ExportMixin, SingleTableView):
    queryset = Stock.objects.annotate(sum_value=Sum('holding__current_value'))
    table_class = StockListTable
    template_name = "portfolio/stock_holding_summary2.html"
    #http://127.0.0.1:8000/stockHoldingsummary2/?_export=csv to download csv of this table
        
class PriceListView(SingleTableView):
    model = Price
    table_class = PriceTable
    template_name = 'portfolio/price.html'
    paginate_by = 10

class HoldingListViewFiltered(ExportMixin,SingleTableMixin, FilterView):
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
    filterset_class = TransactionFilter

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
    accounts_by_person = Account.objects.values('person__name').annotate(total_value=Sum('account_value')).order_by('person__name')
    return render(request, 'portfolio/summary.html', {
    'totals': totals, 'accounts':accounts, 'accounts_by_type': accounts_by_type, 'accounts_by_person': accounts_by_person,
    }, )

class AccountDetailView(DetailView):
    model = Account
    template_name = 'portfolio/account_detail.html'

class TransactionDetailView(DetailView):
    model = Transaction
    template_name = 'portfolio/transaction_detail.html'

class HoldingDetailView(DetailView):
    model = Holding
    template_name = 'portfolio/holding_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        transaction_list = Transaction.objects.filter(account=self.object.account).filter(stock=self.object.stock)
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

@login_required(login_url='/account/login/')
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

        return HttpResponseRedirect(reverse('custom_report') )
    else:
        form = CommandForm()
        context = {
            'form': form
        }
    return render(request, 'portfolio/commands.html', context)

@login_required(login_url='/account/login/')
def recalc(request):
    management.call_command('get_prices')
    management.call_command('refresh_accounts')
    return HttpResponseRedirect(reverse('index') )

def custom_report(request):
    a = Account.objects.filter(person__name = "david") | Account.objects.filter(person__name = "henri")
    total = a.aggregate(Sum('account_value'))
    dtl_pension = Account.objects.filter(person__name = "david", account_type = "pension") 
    a = Account.objects.filter(person__name = "david").exclude(account_type = "pension") | Account.objects.filter(person__name = "henri").exclude(account_type = "pension")
    accounts_by_type = a.values('account_type').annotate(total_value=Sum('account_value'))
    return render(request, 'portfolio/custom_report.html', {
    'total': total, 'dtl_pension':dtl_pension, 'accounts_by_type': accounts_by_type, 
    }, )