from rest_framework.routers import DefaultRouter
from product.views import ProductViewSet
from shop.views import ShopItemsViewSet


router = DefaultRouter()
router.register('product', ProductViewSet)
router.register('shop', ShopItemsViewSet)


