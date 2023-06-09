from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.core.mail import send_mail

from delivery.models import Delivery
from delivery.serializers import DeliverySerializer



class DeliveryViewSet(ModelViewSet):
    queryset = Delivery.objects.all().order_by('-id')
    serializer_class = DeliverySerializer

    @action(methods=['POST'], permission_classes=[IsAuthenticated], detail= False, url_path="create-items")
    def create_delivery(self, request):
        email = request.user.email
        user = User.objects.get(email=email)
        request.data['user_id'] = user.id

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        
        send_mail(
            'Создан предмет доставки',
            f'Создан предмет доставка с id: {serializer.data.get("id")}',
            'admin1@gmail.com',
            ['admin2@gmail.com'],
            fail_silently=True
        )
        
        return Response({'message':'added'})

    @action(methods=['GET'], permission_classes=[IsAuthenticated], detail= False,url_path="items")
    def get_delivery(self, request):
        items = Delivery.objects.all()
        data=DeliverySerializer(items, many=True).data
        return Response(data)

    @action(methods=['PUT'], permission_classes=[IsAuthenticated], detail= True ,url_path="update-items")
    def update_items(self, request, pk):

        if not pk:
            return Response({'error': 'not put'})

        try:
            instance = Delivery.objects.get(id=pk)
        except:
            return Response({'error': 'not put'})


        serializer = self.serializer_class(data=request.data ,instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        send_mail(
            'Обновлен предмет доставки',
            f'Обновлен предмет доставка с id: {serializer.data.get("id")}',
            'admin1@gmail.com',
            ['admin2@gmail.com'],
            fail_silently=True
        )

        return Response({'message': serializer.data})

    @action(methods=['DELETE'], permission_classes=[IsAuthenticated], detail= True, url_path="delete-items")
    def delete_items(self, request, pk):
        if not pk:
            return Response({'error': 'not put'})

        try:
            items = Delivery.objects.get(id=pk)
        except:
            return Response({'error': 'not put'})

        send_mail(
            'Удалена доставка',
            f'Удален предмет доставка с id: {items.id}',
            'admin1@gmail.com',
            ['admin2@gmail.com'],
            fail_silently=True
        )

        items.delete()
        return Response({'message': 'items delete'})