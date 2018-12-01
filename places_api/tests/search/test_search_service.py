# -*- coding: utf-8 -*-
"""
Tests for search services
"""
import mock
import json

from django.urls import reverse
from django.test import TestCase

from rest_framework.test import APIClient

from places_api.serializers import ApiResponseSerializer


class TestSearchService(TestCase):
    """
    Test search services
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
            'search': reverse('api:search')}

    @mock.patch(
        'places_api.utils.gateway.get_info',
        return_value=ApiResponseSerializer(
            json.load(open('places_api/fixtures/mock/full_api_response.json')),
            context={'coords': (19.4719294, -99.1967931)}).data)
    def test_simple_search(self, mock_api_response):
        """
        places search test
        """
        # unauthenticated request
        response = self.user.get(self.services['search'])
        self.assertEqual(response.status_code, 401)
        # user authentication
        self.user.login(
            username='customer@test.com', password='123porPlaces')
        response = self.user.get(self.services['search'], {
            'lat': 19.4719294,
            'long': -99.1967931
        })
        self.assertEqual(response.status_code, 200)
        # checking the individual
        self.assertTrue(response.json()['places'])
        # #checking the individual place info
        self.assertEqual(response.json()['places'][0], {
            'api_id': '77cbfa939e1865ff49880765f853b8df69b0b59f',
            'distance': 876.39256601346,
            'lat': '19.4730008',
            'long': '-99.1885226',
            'name': 'Centennial ballrooms',
            'place_id': 'ChIJ-UlR64H40YURYL3t4Rca1gw',
            'rating': '4.1',
            'vicinity': 'Centenario 367, Nextengo, Ciudad de México'
        })

    def test_simple_search_validation(self):
        """
        test search validation
        """
        # user authentication
        self.user.login(
            username='customer@test.com', password='123porPlaces')
        response = self.user.get(self.services['search'])
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'lat': ['This query param is required'],
            'long': ['This query param is required']
        })

    @mock.patch(
        'places_api.utils.gateway.get_info',
        return_value=ApiResponseSerializer(
            json.load(open('places_api/fixtures/mock/keyword_response.json')),
            context={'coords': (19.4719294, -99.1967931)}).data)
    def test_keyword_search(self, mock_api_response):
        """
        Testing the ordered searches
        """
        # user authentication
        self.user.login(
            username='customer@test.com', password='123porPlaces')

        response = self.user.get(self.services['search'], {
            'lat': 19.4719294,
            'long': -99.1967931,
            'keyword': 'tacos'
        })
        self.assertEqual(response.status_code, 200)
        # this is a keyword search so we compare the raw results to the
        # parsed ones
        # json_file = open('places_api/fixtures/dev/full_api_response.json')
        # response_json = json.load(json_file)
        # response = ApiResponseSerializer(response_json,
        #                            context={'coords': coords})
        # raw_response = json.load(
        #     open('places_api/fixtures/mock/raw_keyword_response.json'))
        # self.assertEqual(len(raw_response['results']),
        #                  len(response.json()['places']))
