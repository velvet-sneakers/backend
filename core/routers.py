from rest_framework.routers import DefaultRouter

from product.views import ProductViewSet
from shop.views import ShopItemsViewSet, ShoesViewSet
from authentication.views import UserViewSet
from delivery.views import DeliveryViewSet


router = DefaultRouter()

router.register('product', ProductViewSet)
router.register('shoes', ShoesViewSet)
router.register('shop', ShopItemsViewSet)
router.register('auth', UserViewSet)
router.register('delivery', DeliveryViewSet)
