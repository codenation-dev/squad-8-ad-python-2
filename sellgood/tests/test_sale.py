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

    def test_last_day_month(self):
        response = self.client.post(reverse('sellgood:sale-list'),
                                    data={'date': '2019-07-01', 
                                          'amount': 1000.0, 
                                          'seller': self.seller1.id},
                                    content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['date'], '2019-07-31')

    def test_unique_sale_month(self):
        mommy.make('Sale', date='2019-07-31', seller=self.seller1)
        response = self.client.post(reverse('sellgood:sale-list'),
                                    data={'date': '2019-07-31', 
                                          'amount': 1000.0, 
                                          'seller': self.seller1.id},
                                    content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['non_field_errors'], 
                                         ['The fields seller, date must make a unique set.'])

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

    def test_partially_update_seller(self): 
        sale = mommy.make('Sale', date='2019-01-01')         
        data = {'id': sale.id, 
                'date': '2019-01-01',               
                'amount': 150.0}          

        response = self.client.patch(reverse('sellgood:sale-detail',                                             kwargs={'pk': sale.id}),
                                   data=data, 
                                   content_type='application/json') 
       
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['amount'], '150.00')
    
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


class NotifyTest(TestCase):
    def setUp(self):
        plan = mommy.make('Plan',
                          minimum_amount=Decimal(10000.0),
                          lower_percentage=Decimal(0.05),
                          higher_percentage=Decimal(0.1))
        
        self.seller = mommy.make('Seller', 
                                 plan=plan, 
                                 email='sellgood@gmail.com')

    def test_one_commission(self):
        response = self.client.post(reverse('sellgood:sale-list'),
                                    data={'date': '2019-01-31', 
                                          'amount': 1000.00, 
                                          'seller': self.seller.id},
                                    content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['notify'], False)

    def test_two_commissions_above(self):
        mommy.make('Sale', 
                   date='2019-01-31', 
                   amount=1000.00, 
                   seller=self.seller)

        response = self.client.post(reverse('sellgood:sale-list'),
                                    data={'date': '2019-02-28', 
                                          'amount': 2000.00, 
                                          'seller': self.seller.id},
                                    content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['notify'], False)

    def test_two_commissions_bellow(self):
        mommy.make('Sale', 
                   date='2019-01-31', 
                   amount=1000.00, 
                   seller=self.seller)

        response = self.client.post(reverse('sellgood:sale-list'),
                                    data={'date': '2019-02-28', 
                                          'amount': 500.00, 
                                          'seller': self.seller.id},
                                    content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['notify'], True)

    def test_three_commissions_above(self):
        mommy.make('Sale', 
                   date='2019-01-31', 
                   amount=1000.00, 
                   seller=self.seller)

        mommy.make('Sale', 
                   date='2019-02-28', 
                   amount=2000.00, 
                   seller=self.seller)

        response = self.client.post(reverse('sellgood:sale-list'),
                                    data={'date': '2019-03-30', 
                                          'amount': 3000.00, 
                                          'seller': self.seller.id},
                                    content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['notify'], False)

    def test_three_commissions_bellow(self):
        mommy.make('Sale', 
                   date='2019-01-31', 
                   amount=1000.00, 
                   seller=self.seller)

        mommy.make('Sale', 
                   date='2019-02-28', 
                   amount=2000.00, 
                   seller=self.seller)

        response = self.client.post(reverse('sellgood:sale-list'),
                                    data={'date': '2019-03-30', 
                                          'amount': 500.00, 
                                          'seller': self.seller.id},
                                    content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['notify'], True)

    def test_four_commissions_above(self):
        mommy.make('Sale', 
                   date='2019-01-31', 
                   amount=2000.00, 
                   seller=self.seller)

        mommy.make('Sale', 
                   date='2019-02-28', 
                   amount=3000.00, 
                   seller=self.seller)

        mommy.make('Sale', 
                   date='2019-03-30', 
                   amount=4000.00, 
                   seller=self.seller)

        response = self.client.post(reverse('sellgood:sale-list'),
                                    data={'date': '2019-04-30', 
                                          'amount': 3000.00, 
                                          'seller': self.seller.id},
                                    content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['notify'], False)

    def test_four_commissions_bellow(self):
        mommy.make('Sale', 
                   date='2019-01-31', 
                   amount=2000.00, 
                   seller=self.seller)

        mommy.make('Sale', 
                   date='2019-02-28', 
                   amount=3000.00, 
                   seller=self.seller)

        mommy.make('Sale', 
                   date='2019-03-30', 
                   amount=4000.00, 
                   seller=self.seller)

        response = self.client.post(reverse('sellgood:sale-list'),
                                    data={'date': '2019-04-30', 
                                          'amount': 1000.00, 
                                          'seller': self.seller.id},
                                    content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['notify'], True)

    def test_five_commissions_above(self):
        mommy.make('Sale', 
                   date='2019-01-31', 
                   amount=2000.00, 
                   seller=self.seller)

        mommy.make('Sale', 
                   date='2019-02-28', 
                   amount=3000.00, 
                   seller=self.seller)

        mommy.make('Sale', 
                   date='2019-03-30', 
                   amount=4000.00, 
                   seller=self.seller)

        mommy.make('Sale', 
                   date='2019-04-30', 
                   amount=3000.00, 
                   seller=self.seller)

        response = self.client.post(reverse('sellgood:sale-list'),
                                    data={'date': '2019-05-31', 
                                          'amount': 4000.00, 
                                          'seller': self.seller.id},
                                    content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['notify'], False)

    def test_five_commissions_bellow(self):
        mommy.make('Sale', 
                   date='2019-01-31', 
                   amount=2000.00, 
                   seller=self.seller)

        mommy.make('Sale', 
                   date='2019-02-28', 
                   amount=3000.00, 
                   seller=self.seller)

        mommy.make('Sale', 
                   date='2019-03-30', 
                   amount=4000.00, 
                   seller=self.seller)

        mommy.make('Sale', 
                   date='2019-04-30', 
                   amount=3000.00, 
                   seller=self.seller)

        response = self.client.post(reverse('sellgood:sale-list'),
                                    data={'date': '2019-05-31', 
                                          'amount': 2000.00, 
                                          'seller': self.seller.id},
                                    content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['notify'], True)

    def test_six_commissions_limit(self):
        mommy.make('Sale', 
                   date='2019-01-31', 
                   amount=7000.00, 
                   seller=self.seller)

        mommy.make('Sale', 
                   date='2019-02-28', 
                   amount=3000.00, 
                   seller=self.seller)

        mommy.make('Sale', 
                   date='2019-03-30', 
                   amount=4000.00, 
                   seller=self.seller)

        mommy.make('Sale', 
                   date='2019-04-30', 
                   amount=3000.00, 
                   seller=self.seller)

        mommy.make('Sale', 
                   date='2019-05-31', 
                   amount=4000.00, 
                   seller=self.seller)

        response = self.client.post(reverse('sellgood:sale-list'),
                                    data={'date': '2019-06-30', 
                                          'amount': 5000.00, 
                                          'seller': self.seller.id},
                                    content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['notify'], False)
