import calendar
from datetime import datetime

from rest_framework import serializers

from sellgood.models import Sale

class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = '__all__'

    def to_internal_value(self, data):
        data = data.copy()
        data['date'] = datetime.strptime(data['date'], '%Y-%m-%d')
        day = calendar.monthrange(data['date'].year, data['date'].month)[1]
        data['date'] = data['date'].replace(day=day).strftime('%Y-%m-%d')
        
        return super().to_internal_value(data)
