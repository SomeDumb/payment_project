from django.contrib import admin
from . models import Item, Order, Price

class PriceInline(admin.TabularInline):
    model = Price

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    inlines = [
        PriceInline,
    ]

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass