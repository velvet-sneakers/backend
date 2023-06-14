from celery import shared_task
from celery.task import periodic_task
from datetime import timedelta
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

@shared_task
def send_email_created_orders(id):
    send_mail(
        'Создан новый заказ',
        f'Создан новый заказ с номером: {id}',
        'admin1@gmail.com',
        ['admin2@gmail.com'],
        fail_silently=True
    )

@periodic_task(run_every=timedelta(minutes=2880))
def send_email_updated_orders(id):
    send_mail(
        'Заказ обновлен',
        f'Обновлен заказ с номером: {id}',
        'admin1@gmail.com',
        ['admin2@gmail.com'],
        fail_silently=True
    )

