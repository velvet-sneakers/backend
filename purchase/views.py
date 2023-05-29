from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from purchase.serializers import PurchaseSerializer
from purchase.models import Purchase
from authentication.models import User


class PurchaseViewSet(ModelViewSet):
    queryset = Purchase.objects.all().order_by('-id')
    serializer_class = PurchaseSerializer

    @action(methods=['POST'], permission_classes=[IsAuthenticated], detail=False, url_path="create-item")
    def create_items(self, request):
        email = request.user.email
        user = User.objects.get(email=email)
        request.data['user_id'] = user.id

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message':'added'})

    @action(methods=['GET'], permission_classes=[IsAuthenticated], detail=False, url_path="items")
    def get_items(self, request):
        items = Purchase.objects.all()
        data = PurchaseSerializer(items, many=True).data
        return Response(data)

    @action(methods=['PUT'], permission_classes=[IsAuthenticated], detail=True, url_path="update-item")
    def update_items(self, request, pk):
        if not pk:
            return Response({'error': 'not put'})

        try:
            instance = Purchase.objects.get(id=pk)
        except:
            return Response({'error': 'not put'})

        serializer = self.serializer_class(data=request.data ,instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': serializer.data})

    @action(methods=['DELETE'], permission_classes=[IsAuthenticated], detail=True, url_path="delete-item")
    def delete_items(self, request, pk):
        if not pk:
            return Response({'error': 'not put'})

        try:
            items = Purchase.objects.get(id=pk)
        except:
            return Response({'error': 'not put'})

        items.delete()
        return Response({'message': 'items delete'})