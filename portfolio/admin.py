from datetime import datetime
from django.contrib import admin
from .models import Transaction, Stock, Account, Price, Holding, Person, HistoricPrice, Dividend

class TransactionInline(admin.TabularInline):
    model = Transaction
    extra = 3

class HoldingInline(admin.TabularInline):
    model = Holding
    extra = 1

class AccountAdmin(admin.ModelAdmin):
    list_display = ('person', 'account_type', 'name', 'account_value')
    inlines = [HoldingInline, TransactionInline]

class PriceAdmin(admin.ModelAdmin):
    list_display = ('date', 'stock', 'price',)
    list_filter = ('stock', )

class HistoricPriceAdmin(admin.ModelAdmin):
    list_display = ('date', 'stock', 'open', 'high', 'low', 'close', 'adjclose')
    list_filter = ('stock', )

class DividendAdmin(admin.ModelAdmin):
    list_display = ('date', 'stock', 'amount',)
    list_filter = ('stock', )

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_type', 'date', 'account', 'stock', 'volume', 'price', 'tcost')
    list_filter = ('account', 'stock')
    search_fields = ['stock']

class HoldingAdmin(admin.ModelAdmin):
    list_display = ('account', 'stock', 'volume', 'current_value', 'book_cost', 'value_updated')
    list_filter = ('account', 'stock', )

def fill_pricehistory(modeladmin, request, queryset):
    for obj in queryset:
        obj.get_historic_prices()

def clear_pricehistory(modeladmin, request, queryset):
    for obj in queryset:
        obj.clear_historic_prices()


class StockAdmin(admin.ModelAdmin):
    list_display = ('name', 'nickname', 'code', 'yahoo_code', 'stock_type', 'current_price', 'price_updated')
    list_filter = ('stock_type', )
    actions = [fill_pricehistory, clear_pricehistory]

class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', )

admin.site.register(Account, AccountAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Price, PriceAdmin)
admin.site.register(HistoricPrice, HistoricPriceAdmin)
admin.site.register(Dividend, DividendAdmin)
admin.site.register(Holding, HoldingAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Stock, StockAdmin)
