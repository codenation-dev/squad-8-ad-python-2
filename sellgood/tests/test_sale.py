import json
from decimal import Decimal
from django.test import Client, TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from sellgood.models import Plan, Seller, Sale

from model_mommy import mommy
from rest_framework import status


class CreateReadSale(TestCase):
    def setUp(self):
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        self.client = Client()
        logged_in = self.client.login(username='testuser', password='12345')

        self.seller1, self.seller2 = mommy.make('sellgood.Seller', _quantity=2)

    def test_create_sale(self):
        data = {
            "date": "2020-12-31",
            "amount": 9191.19,
            "seller": 1,
            }
        response = self.client.post(reverse('sellgood:sale-list'),                                  data=json.dumps(data),                                                  content_type='application/json')

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
        delete_response = self.client.delete(reverse                                                                ('sellgood:sale-list')) 

        self.assertEqual(put_response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(delete_response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_number_sales_recorded(self):
        sale1, sale2, sale3 = mommy.make('sellgood.Sale', _quantity=3, seller=mommy.make('sellgood.Seller'))

        response = self.client.get(reverse('sellgood:sale-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 3)

    def test_detail_sale(self):
        sale1 = mommy.make('sellgood.Sale', amount=1111.56, date='2020-01-31', seller=mommy.make('sellgood.Seller'))
        response = self.client.get(reverse('sellgood:sale-detail', 
                                            kwargs={'pk': 1}))
        
        self.assertEqual(response.json()['id'], 1)
        self.assertEqual(response.json()['date'], '2020-01-31')
        self.assertEqual(float(response.json()['amount']), 1111.56)
    
    def test_update_sale(self):
        sale1, sale2 = mommy.make('sellgood.Sale', _quantity=2, seller=mommy.make('sellgood.Seller'))
        new_sale = {
            'date': "2040-01-31",
            "amount": 25000.00,
            "seller": 2
            }
        
        response = self.client.put(reverse('sellgood:sale-detail',                                                   kwargs={'pk': 1}),  
                                     data=json.dumps(new_sale), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['id'], 1)
        self.assertEqual(response.json()['seller'], 2)
    
    def test_delete_sale(self):
        sale1 = mommy.make('sellgood.Sale', seller=mommy.make('sellgood.Seller'))
        response = self.client.delete(reverse('sellgood:sale-detail',                                          kwargs={'pk': 1}))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_sale_to_delete_not_found(self):
        response = self.client.delete(reverse('sellgood:sale-detail',                                           kwargs={'pk': 8}))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_method_not_allowed(self):
        get_response = self.client.post(reverse('sellgood:sale-detail',                                          kwargs={'pk': 1}))

        self.assertEqual(get_response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class SalesRankMonth(TestCase):
    def setUp(self):
        self.client= Client()
        self.sale1, self.sale2, self.sale3 = create_sales()

    def test_empty_month(self):
        response = self.client.get(reverse('sellgood:sale_rank_month', 
                                            kwargs={'month': 5}))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['error'], 'Empty month')

    def test_number_of_sales_month(self):
        response_jan = self.client.get(reverse('sellgood:sale_rank_month', 
                                                kwargs={'month': 1}))
        response_feb = self.client.get(reverse('sellgood:sale_rank_month', 
                                                kwargs={'month': 2}))

        self.assertListEqual([response_jan.status_code,                                              response_feb.status_code],
                             [200, 200])
        self.assertListEqual([len(response_jan.json()['sales_month']),                               len(response_feb.json()['sales_month'])],
                             [2, 1])

    def test_method_not_allowed(self):
        post_response = self.client.post(reverse('sellgood:sale_rank_month',
                                                 kwargs= {'month': 1}))
        put_response = self.client.put(reverse('sellgood:sale_rank_month',
                                                kwargs= {'month': 1}))
        delete_response = self.client.delete(reverse(
            'sellgood:sale_rank_month',
            kwargs= {'month': 1}))

        self.assertListEqual([post_response.status_code,                                             put_response.status_code, 
                             delete_response.status_code],
                             [405, 405, 405])
        self.assertListEqual([post_response.json()['error'], 
                             put_response.json()['error'], 
                             delete_response.json()['error']],
                             ['Method not allowed', 'Method not allowed', 'Method not allowed'])


class SalesRankYear(TestCase):
    def setUp(self):
        self.client= Client()
        self.sale1, self.sale2, self.sale3 = create_sales()

    
    def test_empty_year(self):
        response = self.client.get(reverse('sellgood:sale_rank_year',
                                            kwargs={'year': 2002}))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['error'], 'Empty year')

    def test_number_sales_year(self):
        response = self.client.get(reverse('sellgood:sale_rank_year',
                                            kwargs={'year': 2020}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['sales_year']), 3)

    def test_method_not_allowed(self):
        post_response = self.client.post(reverse('sellgood:sale_rank_year',
                                                 kwargs= {'year': 2020}))
        put_response = self.client.put(reverse('sellgood:sale_rank_year',
                                                kwargs= {'year': 2020}))
        delete_response = self.client.delete(reverse(
            'sellgood:sale_rank_year',
            kwargs= {'year': 2020}))

        self.assertListEqual([post_response.status_code,                                             put_response.status_code, 
                             delete_response.status_code],
                             [405, 405, 405])
        self.assertListEqual([post_response.json()['error'], 
                             put_response.json()['error'], 
                             delete_response.json()['error']],
                             ['Method not allowed', 'Method not allowed', 'Method not allowed'])


class SalesRankYearMonth(TestCase):
    def setUp(self):
        self.client= Client()
        self.sale1, self.sale2, self.sale3 = create_sales()

    def test_empty_year_month(self):
        response = self.client.get(reverse('sellgood:sale_rank_year_month',
                                            kwargs={'year': 2002, 'month': 1}))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['error'], 'Empty year or empty month')
    
    def test_number_sales_year_month(self):
        response = self.client.get(reverse('sellgood:sale_rank_year_month',
                                            kwargs={'year': 2020, 'month': 1}))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['sale_year_month']), 2)

    def test_method_not_allowed(self):
        post_response = self.client.post(reverse(
            'sellgood:sale_rank_year_month',
            kwargs={'year': 2020, 'month': 1}))
        put_response = self.client.put(reverse(
            'sellgood:sale_rank_year_month',
            kwargs={'year': 2020, 'month': 1}))
        delete_response = self.client.delete(reverse(
            'sellgood:sale_rank_year_month',
            kwargs={'year': 2020, 'month': 1}))

        self.assertListEqual([post_response.status_code,                                             put_response.status_code, 
                             delete_response.status_code],
                             [405, 405, 405])
        self.assertListEqual([post_response.json()['error'], 
                             put_response.json()['error'], 
                             delete_response.json()['error']],
                             ['Method not allowed', 'Method not allowed', 'Method not allowed'])