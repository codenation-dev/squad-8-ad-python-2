from django.conf.urls import url, include
from django.urls import path
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


urlpatterns = [ 
    url(r'^', include(router.urls)),    
    # plan urls
    path('plan', plan.create_plan, name='create_plan'),
    path('plan/get/<int:id>', plan.read_plan, name='get_plan'),
    path('plan/update/<int:id>', plan.update_plan, name='update_plan'),
    path('plan/del/<int:id>', plan.delete_plan, name='delete_plan')
]
