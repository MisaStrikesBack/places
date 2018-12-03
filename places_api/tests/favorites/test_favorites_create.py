# -*- coding: utf-8 -*-
"""
Tests for favorite services
"""
from django.urls import reverse
from django.test import TestCase

from rest_framework.test import APIClient

from places_api.models import Favorite


class TestFavoriteCreateService(TestCase):
    """
    Test favorites create
    """
    fixtures = [
        'dev/users',
        "dev/favorites"
    ]
    maxDiff = None

    def setUp(self):
        """
        Test case setup
        """
        self.user = APIClient()
        self.services = {
            'create': reverse('api:favorites-list')
        }

    def test_create(self):
        """
        Test create service
        """
        # unauthenticated request
        response = self.user.post(self.services['create'])
        self.assertEqual(response.status_code, 401)
        # user authentication
        self.user.login(
            username='customer@test.com', password='123porPlaces')
        # ammount of current favorites
        last_account = Favorite.objects.filter(user_id=1).count()
        # adding  the lat, long query params to post url
        url = "{0}?lat=19.4719294&long=-99.1967931".format(
            self.services['create'])
        # happy request
        response = self.user.post((url), {
            'api_id': 'api_id03',
            'lat': '19.5605360',
            'long': '-99.7683300',
            'name': 'lugar dos',
            'place_id': 'placeid_02',
            'rating': '3.0',
            'vicinity': 'Calle tres',
            'user': 1
            })
        self.assertEqual(response.status_code, 201)
        new_query = Favorite.objects.filter(user_id=1)
        self.assertEqual(last_account + 1, new_query.count())
        # checking lates object inserted in db
        new_favorite = Favorite.objects.last()
        self.assertEqual(response.json()['pk'], new_favorite.pk)
        self.assertEqual(response.json()['name'], new_favorite.name)
        self.assertEqual(1, new_favorite.user.id)

    def test_create_validation(self):
        """
        Creation service validations
        """
        # user authentication
        self.user.login(
            username='customer@test.com', password='123porPlaces')
        # no lat or long in request params
        response = self.user.post(self.services['create'], {})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'lat': ['This query param is required'],
            'long': ['This query param is required']
        })
        # adding  the lat, long query params to post url
        url = "{0}?lat=19.4719294&long=-99.1967931".format(
            self.services['create'])
        # sending empty request body
        response = self.user.post((url))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'api_id': ['This field is required.'],
            'lat': ['This field is required.'],
            'long': ['This field is required.'],
            'name': ['This field is required.'],
            'place_id': ['This field is required.'],
            'user': ['This field is required.'],
            'vicinity': ['This field is required.']
        })
        # adding favorite for another user
        response = self.user.post((url), {
            'api_id': 'api_id03',
            'lat': '19.5605360',
            'long': '-99.7683300',
            'name': 'lugar dos',
            'place_id': 'placeid_02',
            'rating': '3.0',
            'vicinity': 'Calle tres',
            'user': 2
            })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'user': ['Invalid user']
        })
        # adding a favorite id more than once
        response = self.user.post((url), {
            'api_id': 'api_id01',
            'lat': '19.5605360',
            'long': '-99.7683300',
            'name': 'lugar dos',
            'place_id': 'placeid_02',
            'rating': '3.0',
            'vicinity': 'Calle tres',
            'user': 1
            })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'non_field_errors': [
                'The fields api_id, user must make a unique set.'
            ]
        })
        # invalid rating, lat or long value
        response = self.user.post((url), {
            'api_id': 'api_id01',
            'lat': 'not decimal value',
            'long': 'nor decimal value',
            'name': 'lugar dos',
            'place_id': 'placeid_02',
            'rating': 'not decimal value',
            'vicinity': 'Calle tres',
            'user': 1
            })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'lat': ['A valid number is required.'],
            'long': ['A valid number is required.'],
            'rating': ['A valid number is required.']
        })
