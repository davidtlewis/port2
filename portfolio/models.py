from django.db import models

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
        return self.name
    
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
        return (self.transaction_type + " " + str(self.volume) + " " + self.stock.name)

class Price(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, null=True)
    date =  models.DateTimeField(auto_now_add=True, blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    def __str__(self):
        return (self.stock.name + " at " + str(self.date) )