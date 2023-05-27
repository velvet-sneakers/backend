from django.contrib import admin

from shop.models import ShopItems
from shop.models import Shoes


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


class ShoesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'image')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name')
    list_filter = ('name',)


admin.site.register(ShopItems, ShopItemsAdmin)
admin.site.register(Shoes, ShoesAdmin)
