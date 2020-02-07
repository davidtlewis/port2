from django.shortcuts import render
from django.urls import path
from django.http import HttpResponse
from django.views.generic import ListView
from .models import Stock, Price, Holding, Transaction
from django_tables2 import SingleTableView
from .tables import StockTable, HoldingTable, TransactionTable, PriceTable

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
