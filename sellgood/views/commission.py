import json

from rest_framework import generics

from sellgood.models import Sale
from sellgood.serializers import CommissionSerializer


class RankList(generics.ListAPIView):          
    queryset = Sale.objects.all().order_by('-commission')
    serializer_class = CommissionSerializer 
    

class RankYearList(generics.ListAPIView):           
    serializer_class = CommissionSerializer 
    
    def get_queryset(self):
        return (Sale.objects
                    .filter(date__year=self.kwargs['year'])
                    .order_by('-commission'))


class RankMonthList(generics.ListAPIView):           
    serializer_class = CommissionSerializer 
    
    def get_queryset(self):
        return (Sale.objects
                    .filter(date__month=self.kwargs['month'])
                    .order_by('-commission'))


class RankYearMonthList(generics.ListAPIView):           
    serializer_class = CommissionSerializer 
    
    def get_queryset(self):
        return (Sale.objects
                    .filter(date__year=self.kwargs['year'],
                            date__month=self.kwargs['month'])
                    .order_by('-commission'))
