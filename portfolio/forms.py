from django import forms

from .models import Transaction

class TransactionForm(forms.ModelForm):

    class Meta:
        model = Transaction
        fields = ('account', 'transaction_type','date','stock','volume','price','tcost')