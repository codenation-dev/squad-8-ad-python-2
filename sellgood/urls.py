from django.conf.urls import url, include
from rest_framework import routers

from sellgood.views import address, commission, plan, sale, seller


app_name='sellgood'


router = routers.DefaultRouter()
router.register(r'address', address.AddressViewSet, base_name='address')
router.register(r'seller', seller.SellerViewSet, base_name='seller')
router.register(r'sale', sale.SaleViewSet, base_name='sale')
router.register(r'commission',
                commission.CommissionViewSet,
                base_name='commission')
router.register(r'plan', plan.PlanViewSet, base_name='plan')

urlpatterns = [
    url(r'^', include(router.urls))
    ]

