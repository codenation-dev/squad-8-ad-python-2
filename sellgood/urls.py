from django.conf.urls import url, include
from django.urls import path, re_path
from rest_framework import routers

from sellgood.views import address, commission, sale, seller


app_name='sellgood'


router = routers.DefaultRouter()
router.register(r'address', address.AddressViewSet)
router.register(r'seller', seller.SellerViewSet)


urlpatterns = [ 
    url(r'^', include(router.urls)),    
    # sales urls
    path('sale', sale.create_read_sale, name='sale_create_read'),
    path('sale/<int:id_sale>', sale.update_delete_sale,
         name='sale_update_delete'),
    path('sale/seller/<int:id_seller>', sale.sale_list_seller,
         name='sale_seller_read'),
    re_path(r'sale/rank/(?P<month>\d{1,2}$)', sale.list_sales_month,      
            name='sale_rank_month'),
    re_path(r'sale/rank/(?P<year>\d{4}$)', sale.list_sales_year,
            name='sale_rank_year'),
    re_path(r'sale/rank/(?P<year>\d{4})/(?P<month>\d{1,2}$)',   
            sale.list_sales_year_month,                       
            name='sale_rank_year_month'),  
    # commissions urls
    path('commission/', 
         commission.CommissionList.as_view(), 
         name='commission'),
    re_path(r'commission/(?P<year>\d{4})$', 
            commission.CommissionYearList.as_view(), 
            name='commission_year'),
    re_path(r'commission/(?P<month>\d{1,2})$', 
            commission.CommissionMonthList.as_view(), 
            name='commission_month'), 
    path('commission/<int:year>/<int:month>', 
         commission.CommissionYearMonthList.as_view(), 
         name='commission_year_month')
]
