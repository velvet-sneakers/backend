from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.core.mail import send_mail

from delivery.models import Delivery
from delivery.serializers import DeliverySerializer



class DeliveryViewSet(ModelViewSet):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [IsAdminUser()]
        else:
            return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        send_mail(
            'Создана новая доставка',
            f'Создана доставка Order - {response.data.get("order")}, Purchase - {response.data.get("purchase")}',
            'admin1@gmail.com',
            ['admin2@gmail.com'],
            fail_silently=True
        )

        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)

        send_mail(
            'Изменена доставка',
            f'Изменена доставка с id: {response.data.get("id")}',
            'admin1@gmail.com',
            ['admin2@gmail.com'],
            fail_silently=True
        )

        return response

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)

        send_mail(
            'Удалена доставка',
            f'Удалена доставка с id: {response.data.get("id")}',
            'admin1@gmail.com',
            ['admin2@gmail.com'],
            fail_silently=True
        )

        return response