from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from sellgood.models import Address, Seller
from sellgood.serializers import AddressSerializer, SellerSerializer


class SellerViewSet(viewsets.ModelViewSet):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=True)
    def address(self, request, pk=None):
        serializer = AddressSerializer(Address.objects.get(pk=pk))
        return Response(serializer.data)
        