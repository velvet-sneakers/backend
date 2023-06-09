# Generated by Django 4.2 on 2023-05-25 19:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('purchase', '0005_remove_purchase_shop_items'),
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopitems',
            name='purchase',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shop_items', to='purchase.purchase'),
        ),
    ]
