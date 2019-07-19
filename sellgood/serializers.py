from rest_framework import serializers

from sellgood.models import Address, Sale, Seller


class AddressSerializer(serializers.ModelSerializer):       
    class Meta:
        model = Address
        fields = '__all__'


class SellerSerializer(serializers.ModelSerializer):       
    class Meta:
        model = Seller
        fields = '__all__'


class CommissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = ['seller', 'commission']


class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = (
            'id',
            'date',
            'amount',
            'commission',
            'seller'            
        )