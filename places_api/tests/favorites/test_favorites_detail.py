# -*- coding: utf-8 -*-
"""
Tests for favorite services
"""
from django.urls import reverse
from django.test import TestCase

from rest_framework.test import APIClient


class TestFavoriteDetailService(TestCase):
    """
    Test favorites detail service
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
            'detail': reverse('api:favorites-detail', kwargs={'pk': 1})
        }

    def test_detail(self):
        """
        Test favorites detail service
        """
        # unauthenticated request
        response = self.user.get(self.services['detail'])
        self.assertEqual(response.status_code, 401)
        # user authentication
        self.user.login(
            username='customer@test.com', password='123porPlaces')
        response = self.user.get(self.services['detail'], {
            'lat': 19.4719294,
            'long': -99.1967931
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'api_id': 'api_id01',
            'creation_date': '2018-06-14T18:06:14.545000Z',
            'distance': 906.9820976951953,
            'lat': '19.4783580',
            'long': '-99.2021490',
            'name': 'lugar uno',
            'pk': 1,
            'place_id': 'placeid_01',
            'rating': '4.5',
            'vicinity': 'Una calle'
        })

    def test_detail_validation(self):
        """
        Detail query params
        """
        # user authentication
        self.user.login(
            username='customer@test.com', password='123porPlaces')
        # list request
        response = self.user.get(self.services['detail'])
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'lat': ['This query param is required'],
            'long': ['This query param is required']
        })
        # getting the detail from another user
        response = self.user.get(self.services['detail'].replace('1', '4'), {
            'lat': 19.4719294,
            'long': -99.1967931
        })
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {
            'detail': 'Not found.'
        })
        # getting undefined detail
        # getting the detail from another user
        response = self.user.get(self.services['detail'].replace('1', '999'), {
            'lat': 19.4719294,
            'long': -99.1967931
        })
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {
            'detail': 'Not found.'
        })
