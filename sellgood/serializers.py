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
    seller_id = serializers.IntegerField(source='seller.id')
    seller_name = serializers.CharField(source='seller.name')

    class Meta:
        model = Sale
        fields = ['seller_id', 'seller_name', 'id', 'date', 'commission']