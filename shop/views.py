from rest_framework.viewsets import ModelViewSet
from shop.serializers import ShopItemsSerializer
from shop.models import ShopItems


class ShopItemsViewSet(ModelViewSet):
    queryset = ShopItems.objects.all()
    serializer_class = ShopItemsSerializer
