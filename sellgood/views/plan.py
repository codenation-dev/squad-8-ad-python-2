from rest_framework import viewsets

from sellgood.models import Plan
from sellgood.serializers.plan import PlanSerializer


class PlanViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
