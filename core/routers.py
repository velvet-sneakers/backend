from rest_framework.routers import DefaultRouter
from product.views import ProductViewSet
from shop.views import ShopItemsViewSet, ShoesViewSet


router = DefaultRouter()

router.register('product', ProductViewSet)
router.register('shoes', ShoesViewSet)
router.register('shop', ShopItemsViewSet)
