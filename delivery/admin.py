from django.contrib import admin
from delivery.models import Delivery

# class DeliveryAdmin(admin.ModelAdmin):
#     list_display = ('id', 'purchase_id', 'order_id', 'status')
#     fieldsets = (
#         ('Создание Покупки', {
#             'fields': ('id', 'purchase_id', 'order_id', 'status')
#         }),
#         )
#     search_fields = ('id', 'purchase_id', 'order_id', 'status')
#     list_filter = ('id', 'purchase_id', 'order_id', 'status')


admin.site.register(Delivery)
