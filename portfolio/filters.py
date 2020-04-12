import django_filters
from .models import Transaction, Holding


class TransactionByAccountFilter(django_filters.FilterSet):
    class Meta:
        model = Transaction
        fields = ['account',]


class HoldingByAccountFilter(django_filters.FilterSet):
    class Meta:
        model = Holding
        fields = ['account',]