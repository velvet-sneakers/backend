from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from authentication.models import User
from shop.models import Shoes, ShopItems, Order
from shop.serializers import ShoesSerializer, ShopItemsSerializer, OrderSerializer


class ShoesViewSet(ModelViewSet):
    queryset = Shoes.objects.all()
    serializer_class = ShoesSerializer


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

        return response

    def update(self, request, *args, **kwargs):
        email = request.user.email
        user = User.objects.get(email=email)
        request.data['user_id'] = user.id

        response = super().update(request, *args, **kwargs)

        return response


class ShopItemsViewSet(ModelViewSet):
    queryset = ShopItems.objects.all().order_by('-id')
    serializer_class = ShopItemsSerializer

    @action(methods=['POST'],detail= False, url_path="create-items")
    def create_items(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message':'added'})

    @action(methods=['GET'], detail= False,url_path="items")
    def get_items(self, request):
        items = ShopItems.objects.all()
        data=ShopItemsSerializer(items, many=True).data
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
        return Response({'message': serializer.data})

    @action(methods=['DELETE'], detail= True, url_path="delete-items")
    def delete_items(self, request, pk):
        if not pk:
            return Response({'error': 'not put'})

        try:
            items = ShopItems.objects.get(id=pk)
        except:
            return Response({'error': 'not put'})

        items.delete()
        return Response({'message': 'items delete'})
