from sellgood.models import Sale
from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from sellgood.serializers.sale import SaleSerializer


class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer  
    filter_backends = [DjangoFilterBackend]
    filter_fields = {'date': ['year', 'month']}    
