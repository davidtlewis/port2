import django_tables2 as tables
from .models import Stock, Price, Holding, Transaction

class StockTable(tables.Table):
    class Meta:
        model = Stock
        template_name = "django_tables2/bootstrap.html"
        fields = ('code','name', 'stock_type', 'current_price','price_updated')

class PriceTable(tables.Table):
    class Meta:
        model = Price
        template_name = "django_tables2/bootstrap.html"
        #fields = ('price' ,)
        fields = ('stock','date', 'price')
       
class HoldingTable(tables.Table):
    class Meta:
        model = Holding
        template_name = "django_tables2/bootstrap.html"
        fields = ('account','stock', 'volume', 'book_cost','current_value')
        #fields = ('volume', 'book_cost','current_value')

class TransactionTable(tables.Table):
    class Meta:
        model = Transaction
        template_name = "django_tables2/bootstrap.html"
        fields = ('account','stock','transaction_type', 'date', 'volume','price','tcost')
        #fields = ('tcost', )