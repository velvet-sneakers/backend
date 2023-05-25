from rest_framework.viewsets import ModelViewSet

from purchase.serializers import PurchaseSerializer
from purchase.models import Purchase


class PurchaseViewSet(ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
