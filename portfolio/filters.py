import django_filters
from .models import Transaction, Holding, HistoricPrice, Dividend

class TransactionFilter(django_filters.FilterSet):
    class Meta:
        model = Transaction
        fields = ['account','stock']

class HoldingByAccountFilter(django_filters.FilterSet):
    class Meta:
        model = Holding
        fields = ['account','stock','account__person']

class HoldingByAccountFilter2(django_filters.FilterSet):
    class Meta:
        model = Holding
        fields = ['account']

class HistoricPriceByStockFilter(django_filters.FilterSet):
    class Meta:
        model = HistoricPrice
        fields = ['stock',]

class DividendByStockFilter(django_filters.FilterSet):
    class Meta:
        model = Dividend
        fields = ['stock',]