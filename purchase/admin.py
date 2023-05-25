from django.contrib import admin
from purchase.models import Purchase


class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'price', 'shop_items', 'user_id', 'date')
    fieldsets = (
        ('Создание Покупки', {
            'fields': ('price', 'shop_items', 'user_id', 'date')
        }),
    )
    list_display_links = ('id', 'date')
    search_fields = ('id', 'price', 'date')
    list_editable = ('price', 'shop_items')
    list_filter = ('price', 'date')

    row_id_fields = ['shop_items']


admin.site.register(Purchase, PurchaseAdmin)
