from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from sellgood.models import Address, Seller, Sale
from sellgood.serializers.address import AddressSerializer 
from sellgood.serializers.sale import SaleSerializer 
from sellgood.serializers.seller import SellerSerializer 
                        

class SellerViewSet(viewsets.ModelViewSet):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer

    @action(detail=True)
    def address(self, request, pk=None):
        try:
            serializer = AddressSerializer(Address.objects.get(pk=pk))
            return Response(serializer.data)
        except:
            return Response({'detail': 'Not found.'},
                             status=status.HTTP_200_OK)
    
    @action(detail=True)
    def sale(self, request, pk=None):
        query = Sale.objects.filter(seller_id=pk)
        serializer = SaleSerializer(query, many=True)
        if query:
            return Response(serializer.data)
        else:
            return Response({'detail': 'Not found.'}, status=status.HTTP_200_OK)
        