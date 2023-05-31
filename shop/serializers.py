from rest_framework import serializers

from shop.models import ShopItems, Order
from shop.models import Shoes


class ShopItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopItems
        fields = '__all__'

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance

    def update(self, instance, validate_data):
        instance.title = validate_data.get('title', instance.title)
        instance.desc = validate_data.get('desc', instance.desc)
        instance.img = validate_data.get('image', instance.img)
        instance.price = validate_data.get('price', instance.price)
        instance.save()
        return instance




class ShoesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shoes
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
