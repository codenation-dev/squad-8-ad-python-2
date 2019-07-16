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


class UpdateDeleteSales(TestCase):
    def setUp(self):
        self.client= Client()
        self.sale1, self.sale2, self.sale3 = create_sales()

    def test_update_sale(self):
        new_sale = {
            'date': "2040-01-31",
            "amount": 25000.00,
            "seller": 2
            }
        
        response = self.client.put(reverse('sellgood:sale_update_delete',                                                   kwargs={'id_sale': 1}),  
                                     data=json.dumps(new_sale), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['id_sale_updated'][0]['id'], 1)
        

    def test_delete_sale(self):
        response = self.client.delete(reverse('sellgood:sale_update_delete',                                          kwargs={'id_sale': 1}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['id_sale_deleted'], 1)
    
    def test_sale_to_delete_not_found(self):
        response = self.client.delete(reverse('sellgood:sale_update_delete',                                           kwargs={'id_sale': 8}))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['error'], 'sale_id not found')

    def test_method_not_allowed(self):
        get_response = self.client.get(reverse('sellgood:sale_update_delete',                                          kwargs={'id_sale': 1}))
        post_response = self.client.post(reverse('sellgood:sale_update_delete',                                          kwargs={'id_sale': 1}))

        self.assertListEqual([get_response.status_code,                                             post_response.status_code],
                            [405, 405])
        self.assertListEqual([get_response.json()['error'], 
                            post_response.json()['error']], 
                            ['Method not allowed', 'Method not allowed'])


class SaleListSeller(TestCase):
    def setUp(self):
        self.client= Client()
        self.sale1, self.sale2, self.sale3 = create_sales()

    def test_seller_not_found(self):
        response = self.client.get(reverse('sellgood:sale_seller_read', 
                                    kwargs= {'id_seller': 8}))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['error'], 'seller_id not found')

    def test_number_seles_seller(self):
        response_s1 = self.client.get(reverse('sellgood:sale_seller_read',
                                            kwargs= {'id_seller': 1}))
        response_s2 = self.client.get(reverse('sellgood:sale_seller_read',
                                            kwargs= {'id_seller': 2}))

        self.assertListEqual([response_s1.status_code, response_s2.status_code],
                        [200, 200])
        self.assertListEqual([len(response_s1.json()['seller_sales']), 
                              len(response_s2.json()['seller_sales'])],
                              [2, 1])

    def test_method_not_allowed(self):
        post_response = self.client.post(reverse('sellgood:sale_seller_read',
                                            kwargs= {'id_seller': 1}))
        put_response = self.client.put(reverse('sellgood:sale_seller_read',
                                            kwargs= {'id_seller': 1}))
        delete_response = self.client.delete(
                                        reverse('sellgood:sale_seller_read',
                                        kwargs= {'id_seller': 1}))

        self.assertListEqual([post_response.status_code,                                             put_response.status_code, 
                             delete_response.status_code],
                             [405, 405, 405])
        self.assertListEqual([post_response.json()['error'], 
                            put_response.json()['error'], 
                            delete_response.json()['error']],
                            ['Method not allowed', 'Method not allowed', 'Method not allowed'])


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
        self.assertListEqual([len(response_jan.json()['sales_month']),                              len(response_feb.json()['sales_month'])],
                            [2, 1])

    def test_method_not_allowed(self):
        post_response = self.client.post(reverse('sellgood:sale_rank_month',
                                            kwargs= {'month': 1}))
        put_response = self.client.put(reverse('sellgood:sale_rank_month',
                                            kwargs= {'month': 1}))
        delete_response = self.client.delete(
                                        reverse('sellgood:sale_rank_month',
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
        delete_response = self.client.delete(
                                        reverse('sellgood:sale_rank_year',
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
        post_response = self.client.post(reverse                                                                ('sellgood:sale_rank_year_month',
                                        kwargs={'year': 2020, 'month': 1}))
        put_response = self.client.put(reverse('sellgood:sale_rank_year_month',
                                            kwargs={'year': 2020, 'month': 1}))
        delete_response = self.client.delete(
                                        reverse('sellgood:sale_rank_year_month',
                                        kwargs={'year': 2020, 'month': 1}))

        self.assertListEqual([post_response.status_code,                                             put_response.status_code, 
                             delete_response.status_code],
                             [405, 405, 405])
        self.assertListEqual([post_response.json()['error'], 
                            put_response.json()['error'], 
                            delete_response.json()['error']],
                            ['Method not allowed', 'Method not allowed', 'Method not allowed'])