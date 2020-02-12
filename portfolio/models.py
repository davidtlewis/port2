from django.db import models
from django.db.models import Sum

class Account(models.Model):
    name = models.CharField(max_length=50)
    ACCOUNT_TYPE = (
        ('ISA','ISA'),
        ('pension', 'PENSION'),
        ('standard','STANDARD'),
    )
    account_type = models.CharField(max_length=8, choices=ACCOUNT_TYPE, default='buy')
    
    def __str__(self):
        return self.name

class Stock(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=20)
    CURRENCY_TYPE = (
        ('gbp','GBP'),
        ('gbx','GBX'),
        ('usd','USD'),
    )
    currency = models.CharField(max_length=6, choices=CURRENCY_TYPE, default='equity')
    STOCK_TYPE = (
        ('fund','FUND'),
        ('equity','EQUITY'),
        ('etfs','ETFS'),
    )
    stock_type = models.CharField(max_length=6, choices=STOCK_TYPE, default='equity')
    current_price = models.DecimalField(max_digits=7, decimal_places=2)
    price_updated = models.DateTimeField(null=True)
    def __str__(self):
        return self.code + ": " + self.name[:15]
    
class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    TRANSACTION_TYPE = (
        ('buy','BUY'),
        ('sell', 'SELL'),
    )
    transaction_type = models.CharField(max_length=4, choices=TRANSACTION_TYPE, default='buy')
    date = models.DateField()
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, null=True)
    volume = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    tcost = models.DecimalField(max_digits=5, decimal_places=2)
    def __str__(self):
        return (self.transaction_type + " " + str(self.volume) + " " + self.stock.code)

class Price(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, null=True)
    date =  models.DateTimeField(auto_now_add=True, blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    def __str__(self):
        return (self.stock.name + " at " + str(self.date) )

class Holding(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, null=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    volume = models.IntegerField()
    book_cost = models.DecimalField(max_digits = 10, decimal_places=2)
    current_value = models.DecimalField(max_digits = 10, decimal_places=2)
    def __str__(self):
        return (self.stock.name + " in " + str(self.account.name) )

    def refresh_value(self):
        #counter =  Transaction.objects.filter(stock__name=self.stock).count()
        transactions = Transaction.objects.filter(stock=self.stock).filter(account=self.account)
        nett_volume_bought = transactions.filter(transaction_type= 'buy').aggregate(Sum('volume'))['volume__sum']
        if nett_volume_bought is None: nett_volume_bought = 0
        
        nett_volume_sold = transactions.filter(transaction_type= 'sell').aggregate(Sum('volume'))['volume__sum']
        if nett_volume_sold is None: nett_volume_sold = 0
         
        self.volume = nett_volume_bought - nett_volume_sold
        self.current_value = Price.objects.filter(stock=self.stock).latest('date').price * self.volume
        self.save()