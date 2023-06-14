from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.core.mail import send_mail

from delivery.models import Delivery
from delivery.serializers import DeliverySerializer

from delivery.tasks import send_email_created_delivery, send_email_updated_delivery, send_email_deleted_delivery

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

        send_email_created_delivery.delay(response.data.get("id"))

        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)

        send_email_updated_delivery.delay(response.data.get("id"))

        return response

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)

        send_email_deleted_delivery.delay(response.data.get("id"))

        return response