from dal import autocomplete

from django import forms
from . models import Stock


class StockForm(forms.Form):
    Stock = forms.ModelChoiceField(
        queryset = Stock.objects.all(),
        widget=autocomplete.ModelSelect2(
            url='stock-autocomplete',
            attrs={
                'data-placeholder': 'Search for a stock'
            }
        )
    )
    