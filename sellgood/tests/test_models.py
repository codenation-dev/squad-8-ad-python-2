from decimal import Decimal

from django.test import TestCase

from sellgood.models import Sale, Seller, Plan


class SaleModelTests(TestCase):
    def setUp(self):            
        plan = Plan.objects.create(name='senior', 
                                   minimum_amount=Decimal(50000.0),
                                   lower_percentage=Decimal(0.02),
                                   higher_percentage=Decimal(0.1))   

        self.seller = Seller.objects.create(cpf='77711100077', 
                                            name='Bruce Wayne', 
                                            age=30, 
                                            phone='47997001177',
                                            email=('bruce_wayne@'
                                            'wayneenterprises.com'),
                                            plan=plan)

    def test_save_commission_lower(self):
        sale1 = Sale.objects.create(date='2019-06-30', 
                                    amount=50000.00, 
                                    seller=self.seller)        

        sale2 = Sale.objects.create(date='2019-07-31', 
                                    amount=1500.77, 
                                    seller=self.seller)

        self.assertEqual(round(sale1.commission, 2), 
                         round(Decimal(1000.00), 2))        
        self.assertEqual(round(sale2.commission, 2), 
                         round(Decimal(30.02), 2))

    def test_save_commission_higher(self):
        sale1 = Sale.objects.create(date='2019-06-30', 
                                    amount=50000.01, 
                                    seller=self.seller)

        sale2 = Sale.objects.create(date='2019-07-31', 
                                    amount=75700.50, 
                                    seller=self.seller)

        self.assertEqual(round(sale1.commission, 2), 
                         round(Decimal(5000.00), 2))
        self.assertEqual(round(sale2.commission, 2), 
                         round(Decimal(7570.05), 2))
