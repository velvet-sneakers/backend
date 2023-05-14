from rest_framework.routers import DefaultRouter
from product.views import ProductViewSet
from shop.views import ShoesViewSet

router = DefaultRouter()

router.register('product', ProductViewSet)
router.register('shoes', ShoesViewSet)
