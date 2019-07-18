from rest_framework import serializers

from sellgood.models import Address, Sale, Seller

class AddressSerializer(serializers.ModelSerializer):       
    class Meta:
        model = Address
        fields = '__all__'


class CommissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = ['date', 'commission', 'seller']

