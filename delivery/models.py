from django.db import models


class Delivery(models.Model):

    purchase = models.ForeignKey('Purchase', on_delete=models.PROTECT)
    order = models.ForeignKey('Order', on_delete=models.PROTECT)
    status = models.CharField(verbose_name='Статус', max_length=100)

    class Meta:
        verbose_name = 'Доставка'
        verbose_name_plural = 'Доставки'