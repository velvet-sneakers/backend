from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.core.cache import cache
from django.views.decorators.cache import cache_page

from authentication.models import User
from shop.models import Shoes, ShopItems, Order
from shop.serializers import ShoesSerializer, ShopItemsSerializer, OrderSerializer
from .tasks import send_email_created_shoes, send_email_updated_shoes, send_email_created_orders, \
    send_email_updated_orders, send_email_destroyed_shoes, send_email_created_item, send_email_updated_item, \
    send_email_deleted_item

CACHE_SHOES_KEY = 'shoes'
CACHE_TIMEOUT = 3600


class ShoesViewSet(ModelViewSet):
    queryset = Shoes.objects.all()
    serializer_class = ShoesSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        else:
            return [IsAdminUser()]

    @staticmethod
    def set_cache():
        data = ShoesSerializer(Shoes.objects.all(), many=True).data
        cache.set(CACHE_SHOES_KEY, data, timeout=CACHE_TIMEOUT)

        return data

    @action(methods=['GET'], detail=False)
    def get(self, request, *args, **kwargs):
        data = cache.get(CACHE_SHOES_KEY)

        if not data:
            data = self.set_cache()

        return Response(data)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        send_email_created_shoes.delay(response.data.get("name"))

        self.set_cache()

        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)

        send_email_updated_shoes.delay(response.data.get("name"))

        self.set_cache()

        return response

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)

        send_email_destroyed_shoes.delay(response.data.get("id"))

        self.set_cache()

        return response


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [IsAdminUser()]
        else:
            return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        email = request.user.email
        user = User.objects.get(email=email)
        request.data['user_id'] = user.id

        response = super().create(request, *args, **kwargs)

        send_email_created_orders.delay(response.data.get("id"))

        return response

    def update(self, request, *args, **kwargs):
        email = request.user.email
        user = User.objects.get(email=email)
        request.data['user_id'] = user.id

        response = super().update(request, *args, **kwargs)

        send_email_updated_orders.delay(response.data.get("id"))

        return response


class ShopItemsViewSet(ModelViewSet):
    queryset = ShopItems.objects.all().order_by('-id')
    serializer_class = ShopItemsSerializer

    @action(methods=['POST'], detail=False, url_path="create-items")
    def create_items(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        send_email_created_item(serializer.data.get("id"))

        items = ShopItems.objects.all()
        data = ShopItemsSerializer(items, many=True).data
        cache.set('shop_items', data, timeout=CACHE_TIMEOUT)

        return Response({'message': 'added'})

    @action(methods=['GET'], detail=False, url_path="items")
    def get_items(self, request):
        data = cache.get('shop_items')

        if not data:
            items = ShopItems.objects.all()
            data = ShopItemsSerializer(items, many=True).data
            cache.set('shop_items', data, timeout=CACHE_TIMEOUT)
        else:
            print("Fetching data from cache")

        return Response(data)

    @action(methods=['PUT'], detail=True, url_path="update-items")
    def update_items(self, request, pk):
        if not pk:
            return Response({'error': 'not put'})

        try:
            instance = ShopItems.objects.get(id=pk)
        except:
            return Response({'error': 'not put'})

        serializer = self.serializer_class(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        send_email_updated_item.delay(serializer.data.get("id"))

        items = ShopItems.objects.all()
        data = ShopItemsSerializer(items, many=True).data
        cache.set('shop_items', data, timeout=CACHE_TIMEOUT)

        return Response({'data': data})

    @action(methods=['DELETE'], detail= True, url_path="delete-items")
    def delete_items(self, request, pk):
        if not pk:
            return Response({'error': 'not put'})

        try:
            items = ShopItems.objects.get(id=pk)
        except:
            return Response({'error': 'not put'})

        items.delete()

        send_email_deleted_item(items.id)

        items = ShopItems.objects.all()
        data = ShopItemsSerializer(items, many=True).data
        cache.set('shop_items', data, timeout=CACHE_TIMEOUT)

        return Response({'message': 'items delete'})

