from django.urls import path, re_path
from sellgood.views import sale

urlpatterns = [
    # Sale paths - CRUD
    path('sale', sale.create_read_sale, name='sale_create_read'),
    path('sale/<int:id_sale>', sale.update_delete_sale,                             name='sale_update_delete'),

    # Sale list filter by seller
    path('sale/seller/<int:id_seller>', sale.sale_list_seller,                       name='sale_seller_read'),

    # Sale list filter by month - year - year/month
    re_path(r'sale/rank/(?P<month>\d{2}$)', sale.list_sales_month,                       name='sale_rank_month'),
    re_path(r'sale/rank/(?P<year>\d{4}$)', sale.list_sales_year,                       name='sale_rank_year'),
    re_path(r'sale/rank/(?P<year>\d{4})/(?P<month>\d{2}$)',   
            sale.list_sales_year_month,                       name='sale_rank_year_month')
]