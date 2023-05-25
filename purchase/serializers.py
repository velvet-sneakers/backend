from rest_framework import serializers
from purchase.models import Purchase
from shop.serializers import ShopItemsSerializer


class PurchaseSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Purchase
        fields = ['price', 'shop_items', 'user_id', 'date']
