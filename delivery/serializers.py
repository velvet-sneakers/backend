from rest_framework import serializers

from .models import Delivery

class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = ['id', 'purchase_id', 'order_id', 'status']