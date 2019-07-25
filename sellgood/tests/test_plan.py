import json
from decimal import Decimal

from django.test import Client, TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from sellgood.models import Plan, Seller, Sale

from model_mommy import mommy
from rest_framework import status

class PlanViewSet(TestCase):
    def setUp(self):
        self.client = Client()
        

    def test_create_plan(self):
        data = {
            "name": "Entry-level",
            "minimum_amount": "15000.00",
            "lower_percentage": "0.02",
            "higher_percentage": "0.04"
        }

        response = self.client.post(reverse(
            'sellgood:plan-list'),data=json.dumps(data),
             content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['name'], 'Entry-level')

    def test_empty_plan(self):
        response = self.client.get(reverse('sellgood:plan-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 0)
    
    def test_method_not_allowed_list(self):
        response_delete = self.client.delete(reverse('sellgood:plan-list'))
        response_put = self.client.put(reverse('sellgood:plan-list'))

        self.assertEqual(response_delete.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_put.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_number_plan_recorded(self):
        plan1, plan2, plan3 = mommy.make('sellgood.Plan', _quantity=3)
        response = self.client.get(reverse('sellgood:plan-list'))

        self.assertEqual(response.status_code,
                            status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 3)

    def test_detail_plan(self):
        plan1 = mommy.make('sellgood.Plan', name='Entry-Level')

        response = self.client.get(reverse(
            'sellgood:plan-detail', kwargs={'pk':1}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['name'], 'Entry-Level')

    def test_update_plan(self):
        plan1 = mommy.make('sellgood.Plan', name='Entry-Level')
        data = {
            "name": "Platinium",
            "minimum_amount": 20500.00,
            "lower_percentage": 0.08,
            "higher_percentage": 0.11
        }

        response = self.client.put(reverse(
            'sellgood:plan-detail',kwargs={'pk':1}),
            data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['name'], 'Platinium')
        self.assertEqual(response.json()['minimum_amount'], "20500.00")
        self.assertEqual(response.json()['lower_percentage'], "0.08")
        self.assertEqual(response.json()['higher_percentage'], "0.11")