from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
import os


class Shoes(models.Model):
    name = models.CharField(verbose_name='Название обуви', max_length=255)
    image = models.ImageField(verbose_name='Изображение', upload_to='shoes')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Обувь'
        verbose_name_plural = 'Обувь'


# Когда обувь будет удаляться, то и её фотография будет удалятся из media/shoes
@receiver(pre_delete, sender=Shoes)
def delete_image(sender, instance, **kwargs):
    image_path = instance.image.path

    if os.path.exists(image_path):
        os.remove(image_path)
