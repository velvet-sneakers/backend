from rest_framework.routers import DefaultRouter

from product.views import ProductViewSet
from shop.views import ShopItemsViewSet, ShoesViewSet, OrderViewSet
from authentication.views import UserViewSet
from purchase.views import PurchaseViewSet
from delivery.views import DeliveryViewSet

router = DefaultRouter()

router.register('product', ProductViewSet)
router.register('shoes', ShoesViewSet)
router.register('shop', ShopItemsViewSet)
router.register('auth', UserViewSet)
router.register('purchase', PurchaseViewSet)
router.register('order', OrderViewSet)
router.register('delivery', DeliveryViewSet)