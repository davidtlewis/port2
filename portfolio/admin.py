from django.contrib import admin

from .models import Transaction, Stock, Account, Price, Holding
admin.site.register(Transaction)
admin.site.register(Stock)
admin.site.register(Account)
admin.site.register(Price)
admin.site.register(Holding)
