from django.contrib import admin

from .models import Transaction, Stock, Account, Price, Holding

class TransactionInline(admin.TabularInline):
    model = Transaction
    extra = 3

class AccountAdmin(admin.ModelAdmin):
    inlines = [TransactionInline]

admin.site.register(Account, AccountAdmin)
    
admin.site.register(Price)
admin.site.register(Holding)

admin.site.register(Transaction)
admin.site.register(Stock)
