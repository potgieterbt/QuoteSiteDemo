from django.db import models
from django.conf import settings
from django.shortcuts import reverse


class Item(models.Model):
    title = models.CharField(max_length=200)
    code = models.IntegerField(primary_key=True)
    price = models.FloatField()
    notes = models.CharField(max_length=2000)

    def __str__(self):
        template = '{0.title} {0.code} {0.price} {0.notes}'
        return template.format(self)


class QuoteItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    quote_id = models.IntegerField()

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def __str__(self):
        template = '{0.item}, {0.quantity}'
        return template.format(self)


class Quote(models.Model):
    item = models.ManyToManyField(QuoteItem, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    made_date = models.DateTimeField(auto_now_add=True)
    customer = models.CharField(max_length=200)
    address = models.CharField(max_length=500)
    installed = models.BooleanField(default=False)
    total_price = models.FloatField(blank=True, null=True)
    notes = models.CharField(max_length=2000)

    def get_total(self):
        total = 0
        for quoteitem in self.item.all():
            total += quoteitem.get_total_item_price()
            total = round(total, 2)
        return total

    def get_absolute_url(self):
        return reverse("core:quotes", kwargs={"id": self.id})

    def __str__(self):
        return str(self.id)
