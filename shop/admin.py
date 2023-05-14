from django.contrib import admin
from shop.models import ShopItems
# Register your models here.
class ShopItemsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'desc', 'price', 'img')
    fieldsets = (
        ('Создание Предмета', {
            'fields': ('title', 'desc', 'price', 'img')
        }),
    )
    list_display_links = ('id','title',)
    search_fields = ('id', 'title','desc','price',)
    list_editable = ('desc', 'price',)
    list_filter = ( 'price', 'title')





admin.site.register(ShopItems, ShopItemsAdmin)
