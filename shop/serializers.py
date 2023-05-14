from rest_framework import serializers
from django.shortcuts import get_object_or_404
from shop.models import ShopItems


class ShopItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopItems
        fields = '__all__'

    def create_shop_item(price, title, img, desc):
        item = ShopItem(price=price, title=title, img=img, desc=desc)
        item.save()
        return item.id

    # READ
    def get_shop_item(id):
        item = get_object_or_404(ShopItem, id=id)
        return item

    def get_all_shop_items():
        items = ShopItem.objects.all()
        return items

    # UPDATE
    def update_shop_item(id, price=None, title=None, img=None, desc=None):
        item = get_object_or_404(ShopItem, id=id)
        if price is not None:
            item.price = price
        if title is not None:
            item.title = title
        if img is not None:
            item.img = img
        if desc is not None:
            item.desc = desc
        item.save()

    # DELETE
    def delete_shop_item(id):
        item = get_object_or_404(ShopItem, id=id)
        item.delete()
