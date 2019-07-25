from sellgood.views import sale
from sellgood.serializers.commission import CommissionSerializer


class CommissionViewSet(sale.SaleViewSet):
    http_method_names = ['get'] 
    serializer_class = CommissionSerializer      
    ordering = ['-commission']
