from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.core.mail import send_mail
from django.core.cache import cache

from authentication.models import User
from shop.models import Shoes, ShopItems, Order
from shop.serializers import ShoesSerializer, ShopItemsSerializer, OrderSerializer
from .tasks import send_email_created_shoes, send_email_created_orders, send_email_updated_orders


class ShoesViewSet(ModelViewSet):
    queryset = Shoes.objects.all()
    serializer_class = ShoesSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        else:
            return [IsAdminUser()]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        send_email_created_shoes.delay(response.data.get("name"))

        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)

        send_mail(
            'Изменена обувь',
            f'Изменена обувь с id: {response.data.get("id")}',
            'admin1@gmail.com',
            ['admin2@gmail.com'],
            fail_silently=True
        )

        return response

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)

        send_mail(
            'Изменена обувь',
            f'Удалена обувь с id: {response.data.get("id")}',
            'admin1@gmail.com',
            ['admin2@gmail.com'],
            fail_silently=True
        )

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

    @action(methods=['POST'],detail= False, url_path="create-items")
    def create_items(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        send_mail(
            'Создан предмет магазина',
            f'Создан предмет магазина с id: {serializer.data.get("id")}',
            'admin1@gmail.com',
            ['admin2@gmail.com'],
            fail_silently=True
        )

        # Добавляем данные в кеш
        cache.set(f'shop_item_{serializer.data.get("id")}', serializer.data, timeout=3600)

        return Response({'message':'added'})

    @action(methods=['GET'], detail=False, url_path="items")
    def get_items(self, request):
        # Пытаемся получить данные из кеша
        data = cache.get('shop_items')
        if not data:
            print("Fetching data from the database")
            # Если данных в кеше нет, то получаем их из базы данных и добавляем в кеш
            items = ShopItems.objects.all()
            data = ShopItemsSerializer(items, many=True).data
            cache.set('shop_items', data, timeout=3600)
        else:
            #Когда сделаете удалите принты для проверки
            print("Fetching data from cache")

        return Response(data)

    @action(methods=['PUT'], detail= True ,url_path="update-items")
    def update_items(self, request, pk):
        if not pk:
            return Response({'error': 'not put'})

        try:
            instance = ShopItems.objects.get(id=pk)
        except:
            return Response({'error': 'not put'})

        serializer = self.serializer_class(data=request.data ,instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        send_mail(
            'Обновлен предмет магазина',
            f'Обновлен предмет магазина с id: {serializer.data.get("id")}',
            'admin1@gmail.com',
            ['admin2@gmail.com'],
            fail_silently=True
        )

        # Обновляем данные в кеше
        cache.set(f'shop_item_{serializer.data.get("id")}', serializer.data, timeout=3600)

        return Response({'message': serializer.data})

    @action(methods=['DELETE'], detail= True, url_path="delete-items")
    def delete_items(self, request, pk):
        if not pk:
            return Response({'error': 'not put'})

        try:
            items = ShopItems.objects.get(id=pk)
        except:
            return Response({'error': 'not put'})

        send_mail(
            'Удален предмет магазина',
            f'Удален предмет магазина с id: {items.id}',
            'admin1@gmail.com',
            ['admin2@gmail.com'],
            fail_silently=True
        )

        # Удаляем данные из кеша
        cache.delete(f'shop_item_{pk}')

        items.delete()

        return Response({'message': 'items delete'})

