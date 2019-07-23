from rest_framework import generics
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from sellgood.models import Sale
from sellgood.views import sale
from sellgood.serializers.commission import CommissionSerializer


class CommissionViewSet(sale.SaleViewSet):
    http_method_names = ['get'] 
    serializer_class = CommissionSerializer       
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering = ['-commission']
