import json
from decimal import Decimal
from django.test import Client, TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from sellgood.models import Plan, Seller, Sale

from model_mommy import mommy
from rest_framework import status


class SaleViewSetTest(TestCase):
    def setUp(self):
        self.client = Client()
        
        self.seller1, self.seller2 = mommy.make('sellgood.Seller', _quantity=2)

    def test_create_sale(self):
        data = {
            "date": "2020-12-31",
            "amount": 9191.19,
            "seller": 1,
            }
        response = self.client.post(reverse('sellgood:sale-list'),
                                    data=json.dumps(data),
                                    content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['id'], 1)
        self.assertEqual(response.json()['seller'], 1)
        self.assertEqual(float(response.json()['amount']), 9191.19)

    def test_empty_sales(self):
        response = self.client.get(reverse('sellgood:sale-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 0)

    def test_method_not_allowed(self):
        put_response = self.client.put(reverse('sellgood:sale-list'))
        delete_response = self.client.delete(reverse
                                            ('sellgood:sale-list')) 

        self.assertEqual(put_response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(delete_response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_number_sales_recorded(self):
        sale1, sale2, sale3 = mommy.make('sellgood.Sale', _quantity=3,
                                         seller=mommy.make('sellgood.Seller'))

        response = self.client.get(reverse('sellgood:sale-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 3)

    def test_detail_sale(self):
        sale1 = mommy.make('sellgood.Sale', amount=1111.56, date='2020-01-31',
                             seller=mommy.make('sellgood.Seller'))
        response = self.client.get(reverse('sellgood:sale-detail',
                                            kwargs={'pk': 1}))
        
        self.assertEqual(response.json()['id'], 1)
        self.assertEqual(response.json()['date'], '2020-01-31')
        self.assertEqual(float(response.json()['amount']), 1111.56)
    
    def test_update_sale(self):
        sale1, sale2 = mommy.make('sellgood.Sale', _quantity=2,
                                    seller=mommy.make('sellgood.Seller'))
        new_sale = {
            'date': "2040-01-31",
            "amount": 25000.00,
            "seller": 2
            }
        
        response = self.client.put(reverse('sellgood:sale-detail',
                                            kwargs={'pk': 1}),
                                     data=json.dumps(new_sale),
                                     content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['id'], 1)
        self.assertEqual(response.json()['seller'], 2)
    
    def test_delete_sale(self):
        sale1 = mommy.make('sellgood.Sale', 
                            seller=mommy.make('sellgood.Seller'))
        response = self.client.delete(reverse('sellgood:sale-detail',
                                               kwargs={'pk': 1}))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_sale_to_delete_not_found(self):
        response = self.client.delete(reverse('sellgood:sale-detail',
                                                kwargs={'pk': 8}))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_method_not_allowed(self):
        get_response = self.client.post(reverse('sellgood:sale-detail',
                                                kwargs={'pk': 1}))

        self.assertEqual(get_response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)


