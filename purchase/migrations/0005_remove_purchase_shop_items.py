# Generated by Django 4.2 on 2023-05-25 19:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('purchase', '0004_alter_purchase_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchase',
            name='shop_items',
        ),
    ]