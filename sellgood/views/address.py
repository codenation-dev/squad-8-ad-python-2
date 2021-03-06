from rest_framework import viewsets

from sellgood.models import Address
from sellgood.serializers.address import AddressSerializer


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
