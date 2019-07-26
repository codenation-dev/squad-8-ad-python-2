from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status
from model_mommy import mommy


class SellerViewSetTest(TestCase):
    def setUp(self):  
        self.client = Client()
    
    def test_create_seller(self):
        plan = mommy.make('Plan')
        data = {'id': 1,
                'cpf': '77711100077',                 
                'name': 'Bruce', 
                'age': 30,
                'phone': '47997001177', 
                'email': 'bruce_wayne@wayneenterprises.com',
                'plan': plan.id} 

        response = self.client.post(reverse('sellgood:seller-list'), 
                                    data=data, 
                                    content_type='application/json') 
       
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictEqual(response.json(), data)

    def test_read_seller(self):
        seller = mommy.make('Seller', age=30)
               
        response = self.client.get(reverse('sellgood:seller-list'),
                                    content_type='application/json') 
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()[0]['id'], 1)
        self.assertEqual(response.json()[0]['age'], 30)
        
    def test_update_seller(self): 
        seller = mommy.make('Seller')         
        data = {'id': 1,
                'cpf': '77711100077',                 
                'name': 'Bruce', 
                'age': 30,
                'phone': '47997001177', 
                'email': 'bruce_wayne@wayneenterprises.com',
                'plan': seller.plan.id}          

        response = self.client.put(reverse('sellgood:seller-detail',                                             kwargs={'pk': seller.id}),
                                   data=data, 
                                   content_type='application/json') 
       
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.json(), data)

    def test_partially_update_seller(self): 
        seller = mommy.make('Seller')         
        data = {'id': 1,                
                'age': 40}          

        response = self.client.patch(reverse('sellgood:seller-detail',                                             kwargs={'pk': seller.id}),
                                   data=data, 
                                   content_type='application/json') 
       
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['age'], 40)

    def test_delete_seller(self): 
        seller = mommy.make('Seller')                  

        response = self.client.delete(reverse('sellgood:seller-detail',                                             kwargs={'pk': seller.id}),
                                   content_type='application/json') 
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_empty_seller(self):        
        response = self.client.get(reverse('sellgood:seller-list'),
                                    content_type='application/json') 
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 0)

    def test_number_sellers(self):
        mommy.make('Seller', _quantity=5)

        response = self.client.get(reverse('sellgood:seller-list'),
                                    content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 5)

    def test_method_not_allowed(self):
        response = self.client.put(reverse('sellgood:seller-list'),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 
                         status.HTTP_405_METHOD_NOT_ALLOWED)
        