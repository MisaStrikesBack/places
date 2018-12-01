# -*- coding: utf-8 -*-
"""
Tests for auth services
"""
import json

from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User

from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token


class TestUserAuthServices(TestCase):
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
        self.user = APIClient()
        self.services = {
            'login': reverse('api:auth:signin'),
            'logout': reverse('api:auth:signout'),
            'signup': reverse('api:auth:signup'),
            'auth_view': reverse('api:auth:update')
        }

    def test_login_logout(self):
        """
        Testing user login
        """
        # requesting an autenticated only service
        response = self.user.post(self.services['auth_view'])
        self.assertEqual(response.status_code, 401)
        self.assertEqual(json.loads(response.content), {
            'detail': 'Authentication credentials were not provided.'
        })
        # log in service
        response = self.user.post(self.services['login'], {
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
        # loggin user out
        self.user.credentials(
            HTTP_AUTHORIZATION='Token ' + response.data['token'])
        response = self.user.post(self.services['logout'])
        self.assertEqual(response.status_code, 200)
        # checking the user no longer has a token
        self.assertFalse(Token.objects.filter(user_id=1).exists())

    def test_login_validation(self):
        """
        Testing validation in sign in service
        """
        # testing empty post
        response = self.user.post(self.services['login'])
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), {
            'email': ['Please include email'],
            'password': ['Please submit a password']
        })
        # testing wrong email info
        response = self.user.post(self.services['login'], {
            'email': 'customertest.com',
            'password': '123porPlaces'
        })
        self.assertEqual(json.loads(response.content), {
            'email': ['Please use a valid email']
        })
        # testing wrong credentials
        response = self.user.post(self.services['login'], {
            'email': 'customer@test.com',
            'password': 'wrong_credentials'
        })
        self.assertEqual(json.loads(response.content), {
            'detail': 'Login failed: Wrong credentials'
        })

    def test_sign_up(self):
        """
        Testing sign up service
        """
        # testing happy path
        response = self.user.post(self.services['signup'], {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@test.com',
            'password': 'testPassword',
            'confirm_password': 'testPassword'
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.content), {
            "first_name": "Test",
            "last_name": "User",
            "email": "test@test.com"
        })
        # testing sign up with no email
        response = self.user.post(self.services['signup'], {
            'first_name': 'Test002',
            'email': 'test2@test.com',
            'password': 'testPassword',
            'confirm_password': 'testPassword'
        })
        self.assertEqual(response.status_code, 201)

    def test_signup_validation(self):
        """
        Testing validation
        """
        # no request body
        response = self.user.post(self.services['signup'], {})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), {
            'confirm_password': ['This field is required.'],
            'email': ['This field is required.'],
            'first_name': ['This field is required.'],
            'password': ['This field is required.']
        })
        # invalid email info
        response = self.user.post(self.services['signup'], {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testtest.com',
            'password': 'testPassword',
            'confirm_password': 'testPassword'
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), {
            'email': ['Enter a valid email address.']
        })
        # email already in use
        response = self.user.post(self.services['signup'], {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'customer@test.com',
            'password': 'testPassword',
            'confirm_password': 'testPassword'
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), {
            'email': ['The mail is already in use']
        })
        # unmatching passwords
        response = self.user.post(self.services['signup'], {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@test.com',
            'password': 'unmatching_password',
            'confirm_password': 'testPassword'
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), {
            'non_field_errors': ['Passwords do not match']
        })
