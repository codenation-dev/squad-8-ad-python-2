from django.conf.urls import url, include
from django.urls import path, re_path
from rest_framework import routers

from sellgood.views import address, commission, sale, seller


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
]
