from django.contrib import admin

from .models import Transaction, Stock, Account, Price, Holding

class TransactionInline(admin.TabularInline):
    model = Transaction
    extra = 3

class AccountAdmin(admin.ModelAdmin):
    inlines = [TransactionInline]

class PriceAdmin(admin.ModelAdmin):
    list_display = ('date', 'stock', 'price',)
    list_filter = ('stock', )

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('date', 'account', 'stock',)
    list_filter = ('stock', )

class HoldingAdmin(admin.ModelAdmin):
    list_display = ('account', 'stock', 'volume','current_value')
    list_filter = ('stock', )


admin.site.register(Account, AccountAdmin)
    
admin.site.register(Price, PriceAdmin)
admin.site.register(Holding, HoldingAdmin)

admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Stock)
