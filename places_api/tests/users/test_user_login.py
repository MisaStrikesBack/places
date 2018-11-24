# -*- coding: utf-8 -*-
"""
This test has the purpose to verify the correct functioning of AccountInfoView.
"""
import json

from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.auth.models import User

from rest_framework.authtoken.models import Token


class TestUserLogIn(TestCase):
    """
    Test user login service
    """
    fixtures = [
        'dev/users'
    ]
    maxDiff = None

    def setUp(self):
        """
        Test case setup
        """
        self.user = Client()
        self.services = {
            'login': reverse('api:auth:signin'),
            'auth_view': reverse('api:auth:update')
        }

    def test_login(self):
        """
        Testing user login
        """
        # requesting an autenticated only service
        response = self.client.post(self.services['auth_view'])
        self.assertEqual(response.status_code, 401)
        self.assertEqual(json.loads(response.content), {
            'detail': 'Authentication credentials were not provided.'
        })
        # log in service
        response = self.client.post(self.services['login'], {
            'email': 'customer@test.com',
            'password': '123porPlaces'
        })
        # retrieving session token
        session_token = Token.objects.last()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {
            "id": 1,
            "user": "Customer User",
            "token": session_token.key
        })
        # checking the session belongs to the user
        user = User.objects.get(email='customer@test.com')
        self.assertEqual(session_token.user, user)
