from django.forms import ModelForm

from sellgood.models import Plan


class PlanForm(ModelForm):
    class Meta:
        model = Plan
        fields = ['name', 'minimum_amount', 'lower_percentage', 'higher_percentage']