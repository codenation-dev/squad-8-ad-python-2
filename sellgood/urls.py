from django.urls import path
from views import sale

urlpatterns = [
    path('sale/create', sale.create_sale),
    path('sale/update/<int:id_sale>')
]