from django.urls import path, re_path
from sellgood.views import commission
from sellgood.views import sale


app_name='sellgood'
urlpatterns = [
    # Sales urls
    path('sale', sale.create_read_sale, name='sale_create_read'),
    path('sale/<int:id_sale>', sale.update_delete_sale,                             
         name='sale_update_delete'),
    path('sale/seller/<int:id_seller>', sale.sale_list_seller,
         name='sale_seller_read'),
    re_path(r'sale/rank/(?P<month>\d{2}$)', sale.list_sales_month,                       
            name='sale_rank_month'),
    re_path(r'sale/rank/(?P<year>\d{4}$)', sale.list_sales_year,                       
            name='sale_rank_year'),
    re_path(r'sale/rank/(?P<year>\d{4})/(?P<month>\d{2}$)',   
            sale.list_sales_year_month,                       
            name='sale_rank_year_month')  
  
    # Commissions urls
    path('commission/rank/', commission.rank, name='rank'),
    re_path(r'commission/rank/(?P<year>\d{4})$', 
            commission.rank_year, 
            name='rank_year'),
    re_path(r'commission/rank/(?P<month>\d{1,2})$', 
            commission.rank_month, 
            name='rank_month'), 
    path('commission/rank/<int:year>/<int:month>', 
         commission.rank_year_month, 
         name='rank_year_month')
