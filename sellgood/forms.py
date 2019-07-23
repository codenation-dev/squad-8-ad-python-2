from django.forms import ModelForm
from .models import Sale, Plan


class SaleForm(ModelForm):
    class Meta:
        model = Sale
        fields = ['date', 'amount', 'seller']


class PlanForm(ModelForm):
    class Meta:
        model = Plan
        fields = ['name', 'minimum_amount', 'lower_percentage', 'higher_percentage']
