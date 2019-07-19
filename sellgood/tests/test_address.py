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
        self.seller1, self.seller2 = mommy.make('sellgood.Seller', _quantity=2)

    def test_create_address(self):
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
    
        response = self.client.post(reverse('sellgood:address-list'),
                                    data=json.dumps(data),
                                    content_type='application/json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['state'], 'New York')
        self.assertEqual(response.json()['seller'], 1)

    def test_empty_address(self):
        response = self.client.get(reverse('sellgood:address-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 0)
    