from django.contrib import admin
from notification.models import Notification


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'title', 'text', 'date',)
    fieldsets = (
        ('Создание Уведомления', {
            'fields': ('user_id', 'title', 'text', 'date')
        }),
    )
    list_display_links = ('id', 'date')
    search_fields = ('id', 'title', 'date')
    list_filter = ('title', 'date')


admin.site.register(Notification, NotificationAdmin)
