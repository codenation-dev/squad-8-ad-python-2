import json
from decimal import Decimal

from django.test import Client, TestCase
from django.urls import reverse
from django.utils.encoding import force_text
from rest_framework import status
from model_mommy import mommy

from sellgood.models import Sale


class RankListTests(TestCase):
    def setUp(self):
        self.client = Client()

        seller1 = mommy.make('Seller')
        seller2 = mommy.make('Seller')

        mommy.make('Sale',
                   date='2018-12-01',                     
                   seller=seller1)        

        mommy.make('Sale',
                   date='2019-01-13',                    
                   seller=seller1)

        mommy.make('Sale',
                   date='2019-01-22',                    
                   seller=seller2)

    def test_no_records(self):
        Sale.objects.all().delete()
        response = self.client.get(reverse('sellgood:commission_rank'))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 0)
            
    def test_number_of_records(self):
        response = self.client.get(reverse('sellgood:commission_rank'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)             
        self.assertEqual(len(response.json()), 3)

    def test_commissions_order(self):        
        response = self.client.get(reverse('sellgood:commission_rank'))        
        self.assertEqual(response.status_code, status.HTTP_200_OK)             
        for idx, prev in enumerate(response.json()):  
            for next in response.json()[idx+1:]:
                self.assertGreaterEqual(Decimal(prev['commission']), 
                                        Decimal(next['commission']))


class RankYearListTests(TestCase):
    def setUp(self):
        self.client = Client()

        seller1 = mommy.make('Seller')
        seller2 = mommy.make('Seller')

        mommy.make('Sale',
                   date='2018-01-17',                    
                   seller=seller2)    

        mommy.make('Sale',
                   date='2018-12-01',                    
                   seller=seller1)

        mommy.make('Sale',
                   date='2019-01-13',                    
                   seller=seller1)

        mommy.make('Sale',
                   date='2019-01-22',                   
                   seller=seller2)

    def test_no_records(self):        
        response = self.client.get(reverse('sellgood:commission_rank_year', 
                                           kwargs={'year': 2017}))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)             
        self.assertEqual(len(response.json()), 0)
            
    def test_number_of_records(self):
        response = self.client.get(reverse('sellgood:commission_rank_year', 
                                           kwargs={'year': 2019}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)             
        self.assertEqual(len(response.json()), 2)

    def test_commissions_order(self):        
        response = self.client.get(reverse('sellgood:commission_rank_year', 
                                           kwargs={'year': 2019}))     
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)             
        for idx, prev in enumerate(response.json()):
            for next in response.json()[idx+1:]:     
                self.assertGreaterEqual(Decimal(prev['commission']), 
                                        Decimal(next['commission']))


class RankMonthListTests(TestCase):
    def setUp(self):
        self.client = Client()

        seller1 = mommy.make('Seller')
        seller2 = mommy.make('Seller')

        mommy.make('Sale',
                   date='2018-01-17',                   
                   seller=seller2) 

        mommy.make('Sale',
                   date='2019-12-01',                     
                   seller=seller1)  

        mommy.make('Sale',
                   date='2019-01-13',                   
                   seller=seller1)  

        mommy.make('Sale',
                   date='2019-01-22',                   
                   seller=seller2) 

    def test_no_records(self):        
        response = self.client.get(reverse('sellgood:commission_rank_month', 
                                           kwargs={'month': 4}))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)             
        self.assertEqual(len(response.json()), 0)
            
    def test_number_of_records(self):
        response = self.client.get(reverse('sellgood:commission_rank_month', 
                                           kwargs={'month': 1}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)             
        self.assertEqual(len(response.json()), 3)

    def test_commissions_order(self):        
        response = self.client.get(reverse('sellgood:commission_rank_month', 
                                           kwargs={'month': 1}))     
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)             
        for idx, prev in enumerate(response.json()):
            for next in response.json()[idx+1:]:
                self.assertGreaterEqual(Decimal(prev['commission']), 
                                        Decimal(next['commission']))

                            
class RankYearMonthListTests(TestCase):
    def setUp(self):
        self.client = Client()

        seller1 = mommy.make('Seller')
        seller2 = mommy.make('Seller')

        mommy.make('Sale',
                   date='2018-01-17',                   
                   seller=seller2) 

        mommy.make('Sale',
                   date='2019-12-01',                   
                   seller=seller1) 

        mommy.make('Sale',
                   date='2019-01-13',                   
                   seller=seller1)

        mommy.make('Sale',
                   date='2019-01-22',                   
                   seller=seller2) 

    def test_no_records(self):        
        response = self.client.get(reverse(
            'sellgood:commission_rank_year_month', 
            kwargs={'year': 2019, 'month': 4}))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)             
        self.assertEqual(len(response.json()), 0)
            
    def test_number_of_records(self):
        response = self.client.get(reverse(
            'sellgood:commission_rank_year_month', 
            kwargs={'year': 2019, 'month': 1}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)              
        self.assertEqual(len(response.json()), 2)

    def test_commissions_order(self):        
        response = self.client.get(reverse(
            'sellgood:commission_rank_year_month', 
            kwargs={'year': 2019, 'month': 1})) 
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)         
        for idx, prev in enumerate(response.json()):    
            for next in response.json()[idx+1:]:            
                self.assertGreaterEqual(Decimal(prev['commission']), 
                                        Decimal(next['commission']))
