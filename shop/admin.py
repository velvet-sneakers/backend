from django.contrib import admin

from shop.models import Shoes


class ShoesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'image')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name')
    list_filter = ('name',)


admin.site.register(Shoes, ShoesAdmin)
