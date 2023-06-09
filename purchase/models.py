from django.db import models
# from shop.models import ShopItems
from authentication.models import User
from django.utils import timezone

class Purchase(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.price}'

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'
        ordering = ['id']