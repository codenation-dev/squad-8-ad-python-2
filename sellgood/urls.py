from django.urls import path, re_path
from views import sale

urlpatterns = [
    path('sale', sale.create_read_sale),
    path('sale/<int:id_sale>', sale.update_delete_sale),
    path('sale/seller/<int:id_seller>', views.sale_list_seller),
    re_path(r'sale/rank/(?P<month>\d{2}$)', views.list_sales_month,                       name='rank_sale_month'),
    re_path(r'sale/rank/(?P<year>\d{4}$)', views.list_sales_year,                       name='rank_sale_year'),
]