# -*- coding: utf-8 -*-
"""
External api consumption file
"""
import requests
# import json

from django.core.cache import cache

from places_api.constants import API_REQUEST
from places_api.serializers import ApiResponseSerializer


def set_order(url, data):
    """
    this method sets the rank or the radius
    """
    if data.get('order') and data['order'] in ['prominence', 'distance']:
        url = "{0}rankby={1}&".format(url, data['order'])
    else:
        url = "{0}radius=1000&".format(url)
    return url


def set_keyword(url, data):
    """
    this method sets the search keyword if exists
    """
    if data.get('keyword'):
        url = "{0}keyword={1}&".format(url, data['keyword'])
    else:
        url = "{0}type=point_of_interest&".format(url)
    return url


def get_info(data, coords):
    # setting the base url
    url = "{0}location={1},{2}&".format(API_REQUEST, data['lat'], data['long'])
    # if data.get('next_page_token'):
    #     print(len(data['next_page_token']))
    # setting order
    url = set_order(url, data)
    # setting ordering
    url = set_keyword(url, data)
    # checking if the data is
    if cache.get('url') == url:
        print('old query')
        response = cache.get('response')
    else:
        print('cached')
        # setting the
        cache.set('url', url)
        response = ApiResponseSerializer(requests.get(url).json(),
                                         context={'coords': coords})
        cache.set('response', response)
    # json_file = open('places_api/fixtures/dev/full_api_response.json')
    # response_json = json.load(json_file)
    # response = ApiResponseSerializer(response_json,
    #                            context={'coords': coords})
    return response.data
