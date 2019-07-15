import json
from decimal import Decimal

from django.test import Client, TestCase
from django.urls import reverse
from django.utils.encoding import force_text

from sellgood.models import Sale, Seller, Plan


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


class RankViewTests(TestCase):
    def setUp(self):
        self.client = Client()

        seller1, seller2 = create_sellers()

        Sale.objects.create(date='2018-12-01', 
                            amount=50000.00, 
                            seller=seller1)        

        Sale.objects.create(date='2019-01-13', 
                            amount=1500.77, 
                            seller=seller1)

        Sale.objects.create(date='2019-01-22', 
                            amount=44900.77, 
                            seller=seller2)

    def test_no_records(self):
        Sale.objects.all().delete()
        response = self.client.get(reverse('sellgood:commission_rank'), 
                                           args=['no'])
        
        self.assertEqual(response.status_code, 404)              
        self.assertEqual(response.json()['error'], 'rank not found')
            
    def test_number_of_records(self):
        response = self.client.get(reverse('sellgood:commission_rank'))

        self.assertEqual(response.status_code, 200)              
        self.assertEqual(len(response.json()['commission_rank']), 3)

    def test_commissions_order(self):        
        response = self.client.get(reverse('sellgood:commission_rank'))        
        
        self.assertEqual(response.status_code, 200)               
        for idx, prev in enumerate(response.json()['commission_rank']):  
            for next in response.json()['commission_rank'][idx+1:]:
                self.assertGreaterEqual(Decimal(prev['commission']), 
                                        Decimal(next['commission']))


class RankYearViewTests(TestCase):
    def setUp(self):
        self.client = Client()

        seller1, seller2 = create_sellers()

        Sale.objects.create(date='2018-01-17', 
                            amount=55000.00, 
                            seller=seller2) 

        Sale.objects.create(date='2018-12-01', 
                            amount=50000.00, 
                            seller=seller1)        

        Sale.objects.create(date='2019-01-13', 
                            amount=1500.77, 
                            seller=seller1)

        Sale.objects.create(date='2019-01-22', 
                            amount=44900.77, 
                            seller=seller2)

    def test_no_records(self):        
        response = self.client.get(reverse('sellgood:commission_rank_year', 
                                           kwargs={'year': 2017}))
        
        self.assertEqual(response.status_code, 404)              
        self.assertEqual(response.json()['error'], 
                         'rank of year 2017 not found')
            
    def test_number_of_records(self):
        response = self.client.get(reverse('sellgood:commission_rank_year', 
                                           kwargs={'year': 2019}))

        self.assertEqual(response.status_code, 200)              
        self.assertEqual(len(response.json()['commission_rank_year']), 2)

    def test_commissions_order(self):        
        response = self.client.get(reverse('sellgood:commission_rank_year', 
                                           kwargs={'year': 2019}))     
        
        self.assertEqual(response.status_code, 200)               
        for idx, prev in enumerate(response.json()['commission_rank_year']):
            for next in response.json()['commission_rank_year'][idx+1:]:     
                self.assertGreaterEqual(Decimal(prev['commission']), 
                                        Decimal(next['commission']))


class RankMonthViewTests(TestCase):
    def setUp(self):
        self.client = Client()

        seller1, seller2 = create_sellers()

        Sale.objects.create(date='2018-01-17', 
                            amount=55000.00, 
                            seller=seller2) 

        Sale.objects.create(date='2019-12-01', 
                            amount=50000.00, 
                            seller=seller1)        

        Sale.objects.create(date='2019-01-13', 
                            amount=1500.77, 
                            seller=seller1)

        Sale.objects.create(date='2019-01-22', 
                            amount=44900.77, 
                            seller=seller2)

    def test_no_records(self):        
        response = self.client.get(reverse('sellgood:commission_rank_month', 
                                           kwargs={'month': 4}))
        
        self.assertEqual(response.status_code, 404)              
        self.assertEqual(response.json()['error'], 
                         'rank of month 4 not found')
            
    def test_number_of_records(self):
        response = self.client.get(reverse('sellgood:commission_rank_month', 
                                           kwargs={'month': 1}))

        self.assertEqual(response.status_code, 200)              
        self.assertEqual(len(response.json()['commission_rank_month']), 3)

    def test_commissions_order(self):        
        response = self.client.get(reverse('sellgood:commission_rank_month', 
                                           kwargs={'month': 1}))     
        
        self.assertEqual(response.status_code, 200)               
        for idx, prev in enumerate(response.json()['commission_rank_month']):
            for next in response.json()['commission_rank_month'][idx+1:]:
                self.assertGreaterEqual(Decimal(prev['commission']), 
                                        Decimal(next['commission']))

                            
class RankYearMonthViewTests(TestCase):
    def setUp(self):
        self.client = Client()

        seller1, seller2 = create_sellers()

        Sale.objects.create(date='2018-01-17', 
                            amount=55000.00, 
                            seller=seller2) 

        Sale.objects.create(date='2019-12-01', 
                            amount=50000.00, 
                            seller=seller1)        

        Sale.objects.create(date='2019-01-13', 
                            amount=1500.77, 
                            seller=seller1)

        Sale.objects.create(date='2019-01-22', 
                            amount=44900.77, 
                            seller=seller2)

    def test_no_records(self):        
        response = self.client.get(reverse(
            'sellgood:commission_rank_year_month', 
            kwargs={'year': 2019, 'month': 4}))
        
        self.assertEqual(response.status_code, 404)              
        self.assertEqual(response.json()['error'], 
                         'rank of year 2019 and month 4 not found')
            
    def test_number_of_records(self):
        response = self.client.get(reverse(
            'sellgood:commission_rank_year_month', 
            kwargs={'year': 2019, 'month': 1}))

        self.assertEqual(response.status_code, 200)              
        self.assertEqual(len(response.json()['commission_rank_year_month']), 2)

    def test_commissions_order(self):        
        response = self.client.get(reverse(
            'sellgood:commission_rank_year_month', 
            kwargs={'year': 2019, 'month': 1})) 
        
        self.assertEqual(response.status_code, 200) 
        response = response.json()['commission_rank_year_month']
        for idx, prev in enumerate(response):    
            for next in response[idx+1:]:            
                self.assertGreaterEqual(Decimal(prev['commission']), 
                                        Decimal(next['commission']))
