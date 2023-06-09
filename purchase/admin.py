from django.contrib import admin
from purchase.models import Purchase


class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'price', 'user_id', 'date')
    fieldsets = (
        ('Создание Покупки', {
            'fields': ('price', 'user_id', 'date')
        }),
    )
    list_display_links = ('id', 'date')
    search_fields = ('id', 'price', 'date')
    list_filter = ('price', 'date')


admin.site.register(Purchase, PurchaseAdmin)
