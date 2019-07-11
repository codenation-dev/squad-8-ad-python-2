from django.urls import path
from views import sale

urlpatterns = [
    path('sale', sale.create_read_sale),
    path('sale/update/<int:id_sale>')
]