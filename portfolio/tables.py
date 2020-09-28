import django_tables2 as tables
from .models import Stock, Price, Holding, Transaction, Account, HistoricPrice, Dividend
from django_tables2 import A


class StockTable(tables.Table):
    class Meta:
        model = Stock
        template_name = "django_tables2/bootstrap.html"
        fields = ('nickname','code','yahoo_code','name', 'stock_type', 'current_price','price_updated','perf_5y','perf_3y','perf_1y','perf_6m','perf_3m','perf_1m')
    nickname = tables.LinkColumn("stock_detail", args=[A("pk")])

class PriceTable(tables.Table):
    class Meta:
        model = Price
        template_name = "django_tables2/bootstrap.html"
        #fields = ('price' ,)
        fields = ('stock','date', 'price')

class HistoricPriceTable(tables.Table):
    class Meta:
        model = HistoricPrice
        template_name = "django_tables2/bootstrap.html"
        fields = ('date', 'stock', 'open', 'high', 'low', 'close', 'adjclose',  )

class DividendTable(tables.Table):
    class Meta:
        model = Dividend
        template_name = "django_tables2/bootstrap.html"
        fields = ('date','stock', 'amount',  )
       
class HoldingTable(tables.Table):
    class Meta:
        model = Holding
        template_name = "django_tables2/bootstrap.html"
        fields = ('account','stock', 'volume', 'book_cost')
    account = tables.LinkColumn("holding_detail", args=[A("pk")])
    current_value = tables.Column(footer=lambda table: sum(x.current_value for x in table.data)
)

class TransactionTable(tables.Table):
    class Meta:
        model = Transaction
        template_name = "django_tables2/bootstrap.html"
        fields = ('stock','account','transaction_type', 'date', 'volume','price','tcost')
    stock = tables.LinkColumn("transaction_detail", args=[A("pk")])

class AccountTable(tables.Table):
    class Meta:
        model = Account
        template_name = "django_tables2/bootstrap.html"
        fields = ('person','account_type','name','account_value')
    name = tables.LinkColumn("account_detail", args=[A("pk")])