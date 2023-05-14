from django.forms import model_to_dict
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import NotFound
from rest_framework.decorators import action

from shop.models import Shoes
from shop.serializers import ShoesSerializer, UpdateShoesSerializer, DeleteShoesSerializer


class ShoesViewSet(ModelViewSet):
    queryset = Shoes.objects.all()
    serializer_class = ShoesSerializer

    def get_serializer_class(self):
        if self.action == 'update_shoes':
            return UpdateShoesSerializer
        if self.action == 'delete_shoes':
            return DeleteShoesSerializer
        else:
            return ShoesSerializer

    @action(methods=['PATCH'], detail=False, url_path='update')
    def update_shoes(self, request):
        Serializer = self.get_serializer_class()

        serializer = Serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data

        shoe_id = data.get('id')
        name = data.get('name')
        image = data.get('image')

        try:
            shoe = Shoes.objects.get(id=shoe_id)
        except Shoes.DoesNotExist:
            raise NotFound({'error': 'shoes with this id was not found'})

        if name is not None:
            setattr(shoe, 'name', name)

        if image is not None:
            setattr(shoe, 'image', image)

        shoe.save()

        shoes_dict = model_to_dict(shoe)
        serializer = Serializer(data=shoes_dict)
        serializer.is_valid(raise_exception=True)

        return Response({'data': serializer.data})

    @action(methods=['DELETE'], detail=False, url_path='delete')
    def delete_shoes(self, request):
        Serializer = self.get_serializer_class()

        serializer = Serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data

        shoe_id = data.get('id')

        try:
            shoe = Shoes.objects.get(id=shoe_id)
        except Shoes.DoesNotExist:
            raise NotFound({'error': 'shoe with this id was not found'})

        shoe.delete()

        return Response({'message': f'shoe with {shoe_id} was successfully deleted'})
