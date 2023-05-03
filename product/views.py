from rest_framework.viewsets import ModelViewSet
from product.serializers import ProductSerializer
from product.models import Product


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
