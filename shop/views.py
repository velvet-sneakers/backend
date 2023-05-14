from rest_framework.viewsets import ModelViewSet

from shop.models import Shoes
from shop.serializers import ShoesSerializer


class ShoesViewSet(ModelViewSet):
    queryset = Shoes.objects.all()
    serializer_class = ShoesSerializer
