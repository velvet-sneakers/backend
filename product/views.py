from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from authentication.models import User

from product.serializers import ProductSerializer
from product.models import Product
from product.tasks import send_email


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(methods=['POST'], permission_classes=[IsAuthenticated], detail=False, url_path="create-item")
    def create_item(self, request):
        email = request.user.email
        user = User.objects.get(email=email)
        request.data['user_id'] = user.id

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        send_email.delay('Создан продукт', f'Cоздан продукт с id {serializer.data.get("id")}')

        return Response({'message': 'added item'})

    @action(methods=['GET'], permission_classes=[IsAuthenticated], detail=False, url_path="get-items")
    def get_items(self):
        items = Product.objects.all()
        data = ProductSerializer(items, many=True).data
        return Response(data)

    @action(methods=['PUT'], permission_classes=[IsAuthenticated], detail=True, url_path="update-item")
    def update_item(self, request, pk):
        if not pk:
            return Response({'error': 'not put'})

        try:
            instance = Product.objects.get(id=pk)
        except:
            return Response({'error': 'not put'})

        serializer = self.serializer_class(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        send_email.delay('Изменён продукт', f'Изменён продукт с id {serializer.data.get("id")}')

        return Response({'message': serializer.data})

    @action(methods=['DELETE'], permission_classes=[IsAuthenticated], detail=True, url_path="delete-item")
    def delete_item(self, request, pk):
        if not pk:
            return Response({'error': 'not put'})

        try:
            item = Product.objects.get(id=pk)
        except:
            return Response({'error': 'not put'})

        send_email.delay('Удалён продукт', f'Удалён продукт с id {item.id}')

        item.delete()
        return Response({'message': 'deleted item'})
