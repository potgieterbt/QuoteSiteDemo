from django import forms
from .models import Quote, Item
from django.conf import settings


class QuoteForm(forms.ModelForm):
    customer = forms.CharField(max_length=200)
    address = forms.CharField(max_length=500)
    notes = forms.CharField(max_length=2000)

    class Meta:
        model = Quote
        user = {'tag': forms.HiddenInput()}
        fields = [
            'user',
            'customer',
            'address',
            'notes',
        ]


class ItemForm(forms.ModelForm):
    title = forms.CharField(max_length=200)
    code = forms.IntegerField()
    price = forms.FloatField()
    notes = forms.CharField(max_length=2000, required=False)

    class Meta:
        model = Item
        fields = [
            'title',
            'code',
            'price',
            'notes',
        ]
