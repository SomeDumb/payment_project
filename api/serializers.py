from .models import Item, Order
from rest_framework import serializers

class ItemSerializer(serializers.ModelSerializer):
    model = Item
    
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['items',]