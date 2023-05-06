from rest_framework.routers import DefaultRouter
from product.views import ProductViewSet

router = DefaultRouter()
router.register('product', ProductViewSet)
