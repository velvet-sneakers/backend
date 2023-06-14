from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_email_created_shoes(name):
    send_mail(
        'Создана новая обувь',
        f'Создана обувь с именем {name}',
        'admin1@gmail.com',
        ['admin2@gmail.com'],
        fail_silently=True
    )
