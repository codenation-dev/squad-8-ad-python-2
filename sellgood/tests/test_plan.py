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
