from decimal import Decimal
import json

from django.urls import reverse
from django.test import Client, TestCase
from django.contrib.auth.models import User
from rest_framework import status
from model_mommy import mommy

from sellgood.models import Address


class CreateReadUpdateDeleteAddress(TestCase):
    def setUp(self):
        user = User.objects.create(username='testuser')
        user.set_password('123456')
        user.save()
        self.client = Client()
        logged_in = self.client.login(username='testuser', password='123456')
        

    def test_create_address(self):
        seller1 = mommy.make('sellgood.Seller')
        data = {
            'street': 'Main Street',
            'neighborhood': 'Northern Brooklyn',
            'city': 'New York',
            'state': 'New York',
            'number': '5214',
            'complement': 'Apartment 204',
            'zipcode': '10001',
            'seller': 1
            }
    
        response = self.client.post(reverse(
            'sellgood:address-list'), data=json.dumps(data),
            content_type='application/json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['state'], 'New York')
        self.assertEqual(response.json()['seller'], 1)

    def test_empty_address(self):
        response = self.client.get(reverse('sellgood:address-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 0)
    
    def test_method_not_allowed_list(self):
        put_response = self.client.put(reverse('sellgood:address-list'))
        delete_response = self.client.delete(reverse('sellgood:address-list'))

        self.assertEqual(put_response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(delete_response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_number_address_recorded(self):
        address1 = mommy.make('sellgood.Address',
                              seller=mommy.make('sellgood.Seller'))
        address2 = mommy.make('sellgood.Address', 
                              seller=mommy.make('sellgood.Seller'))
        response = self.client.get(reverse('sellgood:address-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)

    def test_detail_address(self):
        address1 = mommy.make(
            'sellgood.Address', city='Arkham', street='Main Street',
             seller=mommy.make('sellgood.Seller'))
        response = self.client.get(reverse('sellgood:address-detail',
                                               kwargs={'pk': 1}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['city'], 'Arkham')
        self.assertEqual(response.json()['street'], 'Main Street')

    def test_update_address(self):
        address1 = mommy.make(
            'sellgood.Address', city='New York', state='New York',
            seller=mommy.make('sellgood.Seller'))
        seller2 = mommy.make('sellgood.Seller')

        data = {
            'street': 'Main Street',
            'neighborhood': 'Northern Brooklyn',
            'city': 'Arkham',
            'state': 'New Jersey',
            'number': '666',
            'complement': 'Apartment 25',
            'zipcode': '10009',
            'seller': 2
            }
        
        response = self.client.put(reverse(
            'sellgood:address-detail', kwargs={'pk': 1}),
            data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['city'], 'Arkham')
        self.assertEqual(response.json()['state'], 'New Jersey')
        self.assertEqual(response.json()['zipcode'], '10009')
        self.assertEqual(response.json()['seller'], 2)

        response2 = self.client.get(reverse('sellgood:address-detail',
                                               kwargs={'pk': 2}))

    def test_delete_address(self):
        address1 = mommy.make('sellgood.Address',
                              seller=mommy.make('sellgood.Seller'))

        response = self.client.delete(reverse(
            'sellgood:address-detail', kwargs={'pk': 1}))
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_address_to_delete_not_found(self):
        address1 = mommy.make('sellgood.Address',
                              seller=mommy.make('sellgood.Seller'))
        
        response = self.client.delete(reverse('sellgood:address-detail',
                                               kwargs={'pk': 2}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_method_not_allowed_detail(self):
        pass