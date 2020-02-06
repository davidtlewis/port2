from django.contrib import admin

from .models import Transaction, Stock, Account
admin.site.register(Transaction)
admin.site.register(Stock)
admin.site.register(Account)
