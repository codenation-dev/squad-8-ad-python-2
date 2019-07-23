from decimal import Decimal

from django.urls import reverse
from django.test import Client, TestCase
from rest_framework import status
from model_mommy import mommy

from sellgood.models import Sale


class CommissionViewSet(TestCase):
    def setUp(self):
        self.client = Client()

        seller1, seller2 = mommy.make('Seller', _quantity=2)
        
        mommy.make('Sale',
                   date='2018-01-31',                     
                   seller=seller1)        

        mommy.make('Sale',
                   date='2019-01-31',                    
                   seller=seller1)

        mommy.make('Sale',
                   date='2019-01-31',                    
                   seller=seller2)

        mommy.make('Sale',
                   date='2019-02-28',                    
                   seller=seller2)    

    def test_no_records(self):
        Sale.objects.all().delete()
        response = self.client.get(reverse('sellgood:commission-list'))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 0)
            
    def test_number_of_records(self):
        response = self.client.get(reverse('sellgood:commission-list'))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)             
        self.assertEqual(len(response.json()), 4)

    def test_commissions_order(self):        
        response = self.client.get(reverse('sellgood:commission-list'))        
        self.assertEqual(response.status_code, status.HTTP_200_OK)             
        for idx, prev in enumerate(response.json()):  
            for next in response.json()[idx+1:]:
                self.assertGreaterEqual(Decimal(prev['commission']), 
                                        Decimal(next['commission']))

    def test_ordering_year(self):
        response = self.client.get('/sellgood/commission/?date__year=2019')

        self.assertEqual(response.status_code, status.HTTP_200_OK)             
        self.assertEqual(len(response.json()), 3)

    def test_ordering_month(self):
        response = self.client.get('/sellgood/commission/?date__month=01')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)             
        self.assertEqual(len(response.json()), 3)

    def test_ordering_year_month(self):
        response = self.client.get('/sellgood/commission/'
                                   '?date__month=01&date__year=2019')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)             
        self.assertEqual(len(response.json()), 2)
