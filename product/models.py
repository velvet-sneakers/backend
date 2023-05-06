from django.db import models


class Product(models.Model):
    title = models.CharField(verbose_name='Название', max_length=255)
    image = models.ImageField(verbose_name='Картинка', upload_to='product')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'