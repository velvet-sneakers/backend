# Generated by Django 4.2 on 2023-05-14 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_remove_shoes_image_after_remove_shoes_image_before_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shoes',
            name='image',
            field=models.ImageField(upload_to='shoes', verbose_name='Изображение'),
        ),
    ]