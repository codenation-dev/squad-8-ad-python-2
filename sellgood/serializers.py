from rest_framework import serializers

from sellgood.models import Sale, Seller


class CommissionSerializer(serializers.ModelSerializer):
    #seller = serializers.PrimaryKeyRelatedField(queryset=Seller.objects.all())
        
    class Meta:
        model = Sale
        fields = ['date', 'commission', 'seller']

