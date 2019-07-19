from decimal import Decimal

from django.test import TestCase
from model_mommy import mommy


class SaleModelTests(TestCase):
    def setUp(self):  
        plan = mommy.make('Plan',
                          minimum_amount=Decimal(50000.0),
                          lower_percentage=Decimal(0.02),
                          higher_percentage=Decimal(0.1))


        self.seller = mommy.make('Seller',
                                 plan=plan)          
        
    def test_save_commission_lower(self):
        sale1 = mommy.make('Sale',                            
                           amount=50000.00, 
                           seller=self.seller)        

        sale2 = mommy.make('Sale',                           
                           amount=1500.77, 
                           seller=self.seller)

        self.assertEqual(round(sale1.commission, 2), 
                         round(Decimal(1000.00), 2))        
        self.assertEqual(round(sale2.commission, 2), 
                         round(Decimal(30.02), 2))

    def test_save_commission_higher(self):
        sale1 = mommy.make('Sale',                             
                           amount=50000.01, 
                           seller=self.seller)

        sale2 = mommy.make('Sale',                           
                           amount=75700.50, 
                           seller=self.seller)

        self.assertEqual(round(sale1.commission, 2), 
                         round(Decimal(5000.00), 2))
        self.assertEqual(round(sale2.commission, 2), 
                         round(Decimal(7570.05), 2))
