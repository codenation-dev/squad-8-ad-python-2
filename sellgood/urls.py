from django.urls import path
from views import sale

urlpatterns = [
    path('sale', sale.create_read_sale),
    path('sale/<int:id_sale>', sale.update_delete_sale),
]