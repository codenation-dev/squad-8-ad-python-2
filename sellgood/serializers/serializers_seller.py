from rest_framework import serializers

from sellgood.models import Seller


class SellerSerializer(serializers.ModelSerializer):       
    class Meta:
        model = Seller
        fields = '__all__'
