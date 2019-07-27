from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from sellgood.models import Sale
from sellgood.serializers.sale import SaleSerializer


class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer  
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filter_fields = {'date': ['year', 'month']}    
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        sale = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data = serializer.data
        data['notify'] = sale.notify()
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        instance = serializer.save()
        return instance
