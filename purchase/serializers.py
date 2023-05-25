from rest_framework import serializers
from purchase.models import Purchase
from shop.serializers import ShopItemsSerializer


class PurchaseSerializer(serializers.ModelSerializer):
    shop_items = ShopItemsSerializer(many=True, read_only=True)

    class Meta:
        model = Purchase
        fields = ['price', 'shop_items', 'user_id', 'date']
