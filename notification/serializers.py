from rest_framework import serializers
from notification.models import Purchase


class NotificationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Purchase
        fields = ['text', 'title', 'user_id', 'date']
