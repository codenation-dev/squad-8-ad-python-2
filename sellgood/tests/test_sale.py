import json
from decimal import Decimal
from django.test import Client, TestCase
from django.urls import reverse
from sellgood.models import Plan, Seller, Sale

def create_sellers():
    plan = Plan.objects.create(name='senior', 
                                minimum_amount=Decimal(50000.0),
                                lower_percentage=Decimal(0.02),
                                higher_percentage=Decimal(0.1))   

    seller1 = Seller.objects.create(cpf='77711100077', 
                                    name='Bruce Wayne', 
                                    age=30, 
                                    phone='47997001177',
                                    email=('bruce_wayne@'
                                    'wayneenterprises.com'),
                                    plan=plan)

    seller2 = Seller.objects.create(cpf='12345678901', 
                                    name='Tony Stark', 
                                    age=32, 
                                    phone='51999001234',
                                    email=('tony.stark@'
                                    'starkindustries.com'),
                                    plan=plan)

    return seller1, seller2

def create_sales():
    seller1, seller2 = create_sellers()
    sale1 = Sale.objects.create(date='2020-01-31',
                                amount=28570.00,
                                seller=seller1)
    sale2 = Sale.objects.create(date='2020-01-30',
                                amount=10000.00,
                                seller=seller2)
    sale3 = Sale.objects.create(date='2020-02-26',
                                amount=5000.00,
                                seller=seller1)
    
    return sale1, sale2, sale3