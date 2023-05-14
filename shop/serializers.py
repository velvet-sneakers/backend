from rest_framework import serializers
from shop.models import Shoes


class ShoesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shoes
        fields = '__all__'


class UpdateShoesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shoes
        fields = '__all__'
        extra_kwargs = {
            'name': {
                'required': False
            },
            'image': {
                'required': False
            },
        }

    def validate(self, attrs):
        if self.initial_data.get('id') is None:
            raise serializers.ValidationError({'error': 'id is required'})

        return self.initial_data


class DeleteShoesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shoes
        fields = ['id']

    def validate(self, attrs):
        if self.initial_data.get('id') is None:
            raise serializers.ValidationError({'error': 'id is required'})

        return self.initial_data
