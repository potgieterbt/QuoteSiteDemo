from django import forms
from .models import Quote, Item
from django.conf import settings


class QuoteForm(forms.ModelForm):
    customer = forms.CharField(max_length=200)
    address = forms.CharField(max_length=500)

    class Meta:
        model = Quote
        fields = [
            'user',
            'customer',
            'address',
        ]


class ItemForm(forms.ModelForm):
    title = forms.CharField(max_length=200)
    code = forms.IntegerField()
    price = forms.FloatField()

    class Meta:
        model = Item
        fields = [
            'title',
            'code',
            'price',
        ]
