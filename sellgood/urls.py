from django.urls import path
from views import sale

urlpatterns = [
    path('sale', sale.create_read_sale),
    path('sale/<int:id_sale>', sale.update_delete_sale),
    path('sale/seller/<int:id_seller>', views.sale_list_seller)
]