from django.shortcuts import render, redirect, get_object_or_404
from .models import Item, Quote, QuoteItem
from django.views.generic import View
from . import forms
from django.core.mail import EmailMessage
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from django.db.models import Q


def Home(request):
    context = {

    }
    template_name = "base.html"
    return render(request, 'home.html', context)


@login_required(login_url='/accounts/login/')
def QuoteView(request):
    context = {
        'quotes': Quote.objects.all(),
    }
    template_name = "quotes.html"
    return render(request, 'quotes.html', context)


@permission_required('quote.add_quote', raise_exception=True)
def NewQuote(request):
    tablehead = ['Title', 'Code', 'Price']
    if request.method == 'POST':
        form = forms.QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            id = Quote.objects.last()
            return redirect('/quotes/%s/add/' % id)
        else:
            form = forms.QuoteForm()
            context = {
                'tablehead': tablehead,
                'form': form,
                'user': request.user,
            }
            return render(request, 'new_quote.html', context)
    else:
        context = {
            'tablehead': tablehead,
            'form': forms.QuoteForm,
            'user': request.user,
        }
        return render(request, 'new_quote.html', context)


def AddItems(request, id):
    tablehead = ['Title', 'Code', 'Price', 'Quantity']
    quote = Quote.objects.get(pk=id)
    if request.method == 'POST':
        i_id = request.POST.get('item_code')
        item = get_object_or_404(Item, pk=i_id)
        quantity = request.POST.get('quantity')
        if quantity == '':
            quantity = 1
        if QuoteItem.objects.filter(item=item, quote_id=id).exists():
            quote_item = QuoteItem.objects.get(item=item, quote_id=id)
        else:
            quote_item = QuoteItem.objects.create(
                item=item, quantity=quantity, quote_id=id)
        if quote.item.filter(item__code=item.code).exists():
            print(type(int(quantity)))
            print(type(quote_item.quantity))
            quote_item.quantity += int(quantity)
            quote_item.save()
            return redirect('/quotes/%s/add/' % id)
        else:
            quote.item.add(quote_item)
            return redirect('/quotes/%s/add/' % id)
    context = {
        'tablehead': tablehead,
        'quote': quote,
        'items': Item.objects.all(),
    }
    return render(request, 'quote_add_item.html', context)


@permission_required('quote_item.delete_quote_item', raise_exception=True)
def RemoveItem(request, id):
    if request.method == 'POST':
        quote = Quote.objects.get(pk=id)
        i_id = request.POST.get('item_code')
        quantity = request.POST.get('item_quantity')
        item = get_object_or_404(Item, pk=i_id)
        quote_item = QuoteItem.objects.filter(item=item, quote_id=id)[0]
        quote.item.remove(quote_item)
        quote_item.delete()
    return redirect('/quotes/%s/add' % id)


@permission_required('quote.delete_quote', raise_exception=True)
def DeleteQuote(request, id):
    quote = Quote.objects.get(pk=id)
    if request.method == 'POST':
        quote.delete()
        return redirect('/quotes')
    else:
        context = {
            'quote': quote,
        }
        return render(request, 'delete_quote.html', context)


@login_required(login_url='/accounts/login/')
def Items(request):
    context = {
        'items': Item.objects.all(),
    }
    return render(request, 'items.html', context)


@permission_required('item.change_item', raise_exception=True)
def ItemEdit(request, code):
    item = Item.objects.get(pk=code)
    form = forms.ItemForm(instance=item)
    if request.method == 'POST':
        form = forms.ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('/items')
        else:
            form = form = forms.ItemForm(instance=item)
    else:
        context = {
            'form': form
        }
        return render(request, 'edit_item.html', context)


def EditItemView(request):
    if request.method == 'POST':
        code = request.POST.get('item_code')
        return redirect('/items/%s/edit' % code)
    items = Item.objects.all()
    context = {
        'items': items,
    }
    return render(request, 'edit_items_view.html', context)


def NewItem(request):
    if request.method == 'POST':
        form = forms.ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/items')
        else:
            form = forms.ItemForm()
    form = forms.ItemForm()
    context = {
        'form': form
    }
    return render(request, 'new_item.html', context)


def ItemDelete(request, code):
    item = Item.objects.get(code=code)
    item.delete()
    return redirect('/items/')


def CSVUpload(request):
    if request.method == 'POST':
        csv_data = []
        new_rows = 0
        changed_rows = 0
        same_rows = 0
        csv = request.FILES["myfile"]
        lines = csv.read().split(b'\r\n')
        del lines[-1]
        for line in lines:
            fields = line.decode("utf-8").split(";")
            data_dict = {}
            data_dict["title"] = fields[0]
            data_dict["code"] = fields[1]
            data_dict["price"] = fields[2]

            if Item.objects.filter(title=fields[0], code=fields[1], price=fields[2]).exists():
                item = Item.objects.get(
                    title=fields[0], code=fields[1], price=fields[2])
                form = forms.ItemForm(data_dict, instance=item)
                if form.is_valid():
                    data_dict["status"] = 'Same'
                    same_rows += 1
                    csv_data.append(data_dict)
            elif Item.objects.filter(code=fields[1]).exists():
                item = Item.objects.get(code=fields[1])
                form = forms.ItemForm(data_dict, instance=item)
                if form.is_valid():
                    data_dict["status"] = 'Changed'
                    changed_rows += 1
                    csv_data.append(data_dict)
                    # form.save()
                else:
                    pass
            else:
                form = forms.ItemForm(data_dict)
                if form.is_valid():
                    data_dict["status"] = 'New'
                    new_rows += 1
                    csv_data.append(data_dict)
                else:
                    pass
    context = {
        'new_rows': new_rows,
        'changed_rows': changed_rows,
        'same_rows': same_rows,
        'items_len': len(csv_data),
        'items': csv_data,
        'csv': lines,
    }
    return render(request, 'items_in_csv.html', context)


def AddItemCSV(request):
    if request.method == 'POST':
        csv_data = []
        csv = request.POST.get('csv')
        csv = csv.replace('[b\'', '').replace('\']', '').replace(
            'b\'', '').replace('\'', '')
        print(csv)
        for item in csv.split(','):
            print(item)
            csv_data.append(item)
        if csv is not None:
            print(csv)
            for line in csv_data:
                print(line)
                fields = line.split(";")
                data_dict = {}
                data_dict["title"] = fields[0]
                data_dict["code"] = fields[1]
                data_dict["price"] = fields[2]
                if Item.objects.filter(title=fields[0], code=fields[1], price=fields[2]).exists():
                    pass
                elif Item.objects.filter(code=fields[1]).exists():
                    item = Item.objects.get(code=fields[1])
                    form = forms.ItemForm(data_dict, instance=item)
                    if form.is_valid():
                        form.save()
                        print('Item Saved')
                    else:
                        pass
                else:
                    form = forms.ItemForm(data_dict)
                    if form.is_valid():
                        form.save()
                        print('Item Saved')
                    else:
                        pass
    return redirect('/items/')


@login_required(login_url='/accounts/login/')
def UserProfile(request):
    quotes = Quote.objects.filter(user=request.user)
    context = {
        'user': request.user,
        'quotes': quotes,
    }
    return render(request, 'profile.html', context)


def SendPDFEmail(request, id):
    pass
    email = EmailMessage(
        'Hello',
        'Body goes here',
        'from@example.com',
    )
    email.attach_file('/pdf/%s.pdf' % id)


def QuoteDetail(request, id):
    quote = Quote.objects.get(pk=id)
    context = {
        'user': request.user,
        'quote': quote,
    }
    return render(request, 'quote_detail.html', context)


def Search(request):
    context = {}
    queryset = []
    q = request.GET.get('q')
    sort_by = request.GET.get('order_by')
    if q:
        context['query'] = q
        items = Item.objects.filter(
            Q(title__icontains=q) |
            Q(code__icontains=q)
        ).distinct()
        context['items'] = items
    else:
        items = Item.objects.all()
        context['items'] = items
    if sort_by:
        context['sort_by'] = sort_by
        items = items.order_by(sort_by)
        context['items'] = items
    return render(request, 'search.html', context)