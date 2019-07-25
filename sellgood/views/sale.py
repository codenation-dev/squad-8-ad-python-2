from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter

from sellgood.models import Sale
from sellgood.serializers.sale import SaleSerializer


class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer  
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filter_fields = {'date': ['year', 'month']}    
    ordering = ['-date']