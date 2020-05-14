from django.urls import path, reverse
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.Home, name='home'),

    path('quotes/', views.QuoteView, name='quotes'),
    path('quotes/new/', views.NewQuote, name='new quote'),
    path('quotes/<id>/add/', views.AddItems, name='add items'),
    path('quotes/<id>/delete/', views.RemoveItem, name='remove item'),
    path('quotes/<id>/remove/', views.DeleteQuote, name='delete quote'),
    path('quotes/<id>/email/', views.SendPDFEmail, name='Send Email'),
    path('quotes/<id>/', views.QuoteDetail, name='Quote_Detail'),
    path('quotes/<id>/installed/',
         views.ChangedInstalled, name="install change"),
    path('quotes/search/', views.QuoteSearch, name="search"),

    path('items/', views.Items, name='items'),
    path('items/new/', views.NewItem, name='new item'),
    path('items/edit/', views.EditItemView, name='edit item view'),
    path('items/<code>/edit/', views.ItemEdit, name='edit item'),
    path('items/<code>/remove/', views.ItemDelete, name='delete item'),
    path('items/upload/', views.AddItemCSV, name='Upload csv'),
    path('items/csvcheck/', views.CSVUpload, name='csv upload'),
    path('items/search/', views.ItemSearch, name="search"),

    path('accounts/profile/', views.UserProfile, name='profile'),
]
