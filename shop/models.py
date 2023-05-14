from django.db import models

# Create your models here.
class ShopItems(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    img = models.ImageField(upload_to='shop', verbose_name='Фото товара')
    title = models.CharField(verbose_name='Название товара', max_length=255)
    desc = models.TextField(verbose_name='Описание товара')


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['id', 'title']
