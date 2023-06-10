from django.db import models
from shop.models import Order
from purchase.models import Purchase

class Delivery(models.Model):

    purchase = models.ForeignKey(Purchase, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    status = models.CharField(verbose_name='Статус', max_length=100)

    class Meta:
        verbose_name = 'Доставка'
        verbose_name_plural = 'Доставки'
        ordering = ['id']