from django.shortcuts import render
from django.urls import path
from django.http import HttpResponse
from django.views.generic import ListView
from .models import Stock, Price
from django_tables2 import SingleTableView
from .tables import StockTable

def home(request):
    return HttpResponse("Hello, Django!")

class StockListView(SingleTableView):
    model = Stock
    table_class = StockTable
    template_name = 'portfolio/stocks.html'

class PriceListView(ListView):
    model = Price
    template_name = 'portfolio/stocks.html'

#def stock_list(request):
#    stocks = Stock(objects.all()
#    return HttpResponse("list of the stocks")




