from rest_framework import viewsets, permissions

from sellgood.models import Seller
from sellgood.serializers import SellerSerializer


class SellerViewSet(viewsets.ModelViewSet):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]