from rest_framework.viewsets import ModelViewSet
from shop.serializers import ShopItemsSerializer
from shop.models import ShopItems
from rest_framework.decorators import action
from rest_framework.response import Response


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
