from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache

from purchase.serializers import PurchaseSerializer
from purchase.models import Purchase
from authentication.models import User
from purchase.tasks import send_email_created_purchase, send_email_updated_purchase, send_email_deleted_purchase


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

        send_email_created_purchase.delay(serializer.data.get("id"))

        items = Purchase.objects.all()
        data = PurchaseSerializer(items, many=True).data
        cache.set('purchase_items', data, timeout=3600)

        return Response({'message':'added'})

    @action(methods=['GET'], permission_classes=[IsAuthenticated], detail=False, url_path="items")
    def get_items(self, request):
        data = cache.get('purchase_items')
        if not data:
            items = Purchase.objects.all()
            data = PurchaseSerializer(items, many=True).data
            cache.set('purchase_items', data, timeout=3600)
        else:
            print("Fetching data from cache")

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

        send_email_updated_purchase.delay(serializer.data.get("id"))

        items = Purchase.objects.all()
        data = PurchaseSerializer(items, many=True).data
        cache.set('purchase_items', data, timeout=3600)

        return Response({'message': serializer.data})

    @action(methods=['DELETE'], permission_classes=[IsAuthenticated], detail=True, url_path="delete-item")
    def delete_items(self, request, pk):
        if not pk:
            return Response({'error': 'not put'})

        try:
            items = Purchase.objects.get(id=pk)
        except:
            return Response({'error': 'not put'})

        send_email_deleted_purchase.delay(items.id)

        items = Purchase.objects.all()
        data = PurchaseSerializer(items, many=True).data
        cache.set('purchase_items', data, timeout=3600)

        items.delete()
        return Response({'message': 'items delete'})