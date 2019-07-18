from sellgood.models import Sale
from rest_framework import generics, viewsets
from sellgood.serializers import SaleSerializer


class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer  


class ListSaleYearMonth(generics.ListAPIView):
    serializer_class = SaleSerializer

    def get_queryset(self):
        month = self.kwargs.get('month')
        year = self.kwargs.get('year')
        if month and not year:
            return Sale.objects.filter(date__month=month)
        elif year and not month:
            return Sale.objects.filter(date__year=year)
        elif year and month:
            return Sale.objects.filter(date__year=year, date__month=month)