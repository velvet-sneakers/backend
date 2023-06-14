from django.db import models
from authentication.models import User
from django.utils import timezone

class Notification(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    title = models.TextField(verbose_name='Заголовок уведомления')
    text = models.TextField(verbose_name='Текст уведомления')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'
        ordering = ['id', 'title']