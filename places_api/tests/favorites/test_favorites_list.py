# -*- coding: utf-8 -*-
"""
Tests for favorite services
"""
from django.urls import reverse
from django.test import TestCase

from rest_framework.test import APIClient


class TestFavoriteListService(TestCase):
    """
    Test favorites list service
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
            'list': reverse('api:favorites-list')
        }

    def test_list(self):
        """
        Test favorites list service
        """
        # unauthenticated request
        response = self.user.get(self.services['list'])
        self.assertEqual(response.status_code, 401)
        # user authentication
        self.user.login(
            username='customer@test.com', password='123porPlaces')
        response = self.user.get(self.services['list'], {
            'lat': 19.4719294,
            'long': -99.1967931
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'count': 2,
            'next': None,
            'previous': None,
            'results': [
                {
                    'api_id': 'api_id02',
                    'creation_date': '2018-06-13T18:06:14.545000Z',
                    'distance': 3243.726992572316,
                    'lat': '19.4605360',
                    'long': '-99.1683300',
                    'name': 'lugar dos',
                    'pk': 2,
                    'place_id': 'placeid_02',
                    'rating': '4.9',
                    'vicinity': 'Dos calle'
                },
                {
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
                }
            ]
        })

    def test_list_validation(self):
        """
        checking list queryparams validation
        """
        # user authentication
        self.user.login(
            username='customer@test.com', password='123porPlaces')
        # list request
        response = self.user.get(self.services['list'])
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'lat': ['This query param is required'],
            'long': ['This query param is required']
        })

    def test_list_date_ordering(self):
        """
        Date time ordering test
        """
        # user authentication
        self.user.login(
            username='customer@test.com', password='123porPlaces')
        # list request newer
        response = self.user.get(self.services['list'], {
            'lat': 19.4719294,
            'long': -99.1967931,
            'order': 'newer'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'count': 2,
            'next': None,
            'previous': None,
            'results': [
                {
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
                },
                {
                    'api_id': 'api_id02',
                    'creation_date': '2018-06-13T18:06:14.545000Z',
                    'distance': 3243.726992572316,
                    'lat': '19.4605360',
                    'long': '-99.1683300',
                    'name': 'lugar dos',
                    'pk': 2,
                    'place_id': 'placeid_02',
                    'rating': '4.9',
                    'vicinity': 'Dos calle'
                }
            ]
        })
        # list request older
        response = self.user.get(self.services['list'], {
            'lat': 19.4719294,
            'long': -99.1967931,
            'order': 'older'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'count': 2,
            'next': None,
            'previous': None,
            'results': [
                {
                    'api_id': 'api_id02',
                    'creation_date': '2018-06-13T18:06:14.545000Z',
                    'distance': 3243.726992572316,
                    'lat': '19.4605360',
                    'long': '-99.1683300',
                    'name': 'lugar dos',
                    'pk': 2,
                    'place_id': 'placeid_02',
                    'rating': '4.9',
                    'vicinity': 'Dos calle'
                },
                {
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
                }
            ]
        })

    def test_list_rating_ordering(self):
        """
        Rating time ordering test
        """
        # user authentication
        self.user.login(
            username='customer@test.com', password='123porPlaces')
        # list request better
        response = self.user.get(self.services['list'], {
            'lat': 19.4719294,
            'long': -99.1967931,
            'order': 'better'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'count': 2,
            'next': None,
            'previous': None,
            'results': [
                {
                    'api_id': 'api_id02',
                    'creation_date': '2018-06-13T18:06:14.545000Z',
                    'distance': 3243.726992572316,
                    'lat': '19.4605360',
                    'long': '-99.1683300',
                    'name': 'lugar dos',
                    'pk': 2,
                    'place_id': 'placeid_02',
                    'rating': '4.9',
                    'vicinity': 'Dos calle'
                },
                {
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
                }
            ]
        })
        # list request worst
        response = self.user.get(self.services['list'], {
            'lat': 19.4719294,
            'long': -99.1967931,
            'order': 'worst'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'count': 2,
            'next': None,
            'previous': None,
            'results': [
                {
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
                },
                {
                    'api_id': 'api_id02',
                    'creation_date': '2018-06-13T18:06:14.545000Z',
                    'distance': 3243.726992572316,
                    'lat': '19.4605360',
                    'long': '-99.1683300',
                    'name': 'lugar dos',
                    'pk': 2,
                    'place_id': 'placeid_02',
                    'rating': '4.9',
                    'vicinity': 'Dos calle'
                }
            ]
        })

    def test_list_distance_ordering(self):
        """
        Distance time ordering test
        """
        # user authentication
        self.user.login(
            username='customer@test.com', password='123porPlaces')
        # list request near
        response = self.user.get(self.services['list'], {
            'lat': 19.4719294,
            'long': -99.1967931,
            'order': 'near'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'count': 2,
            'next': None,
            'previous': None,
            'results': [
                {
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
                },
                {
                    'api_id': 'api_id02',
                    'creation_date': '2018-06-13T18:06:14.545000Z',
                    'distance': 3243.726992572316,
                    'lat': '19.4605360',
                    'long': '-99.1683300',
                    'name': 'lugar dos',
                    'pk': 2,
                    'place_id': 'placeid_02',
                    'rating': '4.9',
                    'vicinity': 'Dos calle'
                }
            ]
        })
        # list request worst
        response = self.user.get(self.services['list'], {
            'lat': 19.4719294,
            'long': -99.1967931,
            'order': 'far'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'count': 2,
            'next': None,
            'previous': None,
            'results': [
                {
                    'api_id': 'api_id02',
                    'creation_date': '2018-06-13T18:06:14.545000Z',
                    'distance': 3243.726992572316,
                    'lat': '19.4605360',
                    'long': '-99.1683300',
                    'name': 'lugar dos',
                    'pk': 2,
                    'place_id': 'placeid_02',
                    'rating': '4.9',
                    'vicinity': 'Dos calle'
                },
                {
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
                }
            ]
        })
