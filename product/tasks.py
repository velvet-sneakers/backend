from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_email(title, message):
    send_mail(
        title,
        message,
        'admin1@gmail.com',
        ['admin2@gmail.com'],
        fail_silently=True
    )
