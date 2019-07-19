from sellgood.models import Sale
from rest_framework import generics, viewsets, permissions
from sellgood.serializers import SaleSerializer


class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer  
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
