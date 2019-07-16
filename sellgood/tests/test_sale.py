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


class CreateReadSale(TestCase):
    def setUp(self):
        self.client = Client()
        self.seller1, self.seller2 = create_sellers()

    def test_create_sale(self):
        data = {
            "date": "2020-12-31",
            "amount": 9191.19,
            "seller": 1,
            }
        response = self.client.post(reverse('sellgood:sale_create_read'),                                  data=json.dumps(data),                                                  content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['New Sale Info'][0]['id'], 1)
        self.assertEqual(response.json()['New Sale Info'][0]['seller'], 1)
        self.assertEqual(float(response.json()['New Sale Info'][0]['amount']), 9191.19)

    def test_empty_sales(self):
        response = self.client.get(reverse('sellgood:sale_create_read'))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['error'], 'no sales recorded')

    def test_method_not_allowed(self):
        put_response = self.client.put(reverse('sellgood:sale_create_read'))
        delete_response = self.client.delete(reverse                                                                ('sellgood:sale_create_read')) 

        self.assertEqual(put_response.status_code, 405)
        self.assertEqual(delete_response.status_code, 405)
        self.assertListEqual([put_response.json()['error'], 
                            delete_response.json()['error']], ['Method not allowed', 'Method not allowed'])
    
    def test_number_sales_recorded(self):
        sale1, sale2, sale3 = create_sales()

        response = self.client.get(reverse('sellgood:sale_create_read'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["sales"]), 3)