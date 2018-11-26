# -*- coding: utf-8 -*-
"""
External api consumption file
"""
import requests

from django.core.cache import cache

from places_api.constants import api_request
from places_api.serializers import PlaceSerializer


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
    url = "{0}location={1},{2}&".format(api_request, data['lat'], data['long'])
    # setting order
    url = set_order(url, data)
    # setting ordering
    url = set_keyword(url, data)
    # checking if the data is
    if cache.get('url') == url:
        print('old query')
        response = cache.get('response')
    else:
        # setting the
        cache.set('url', url)

        response = PlaceSerializer(requests.get(url).json()['results'],
                                   many=True,
                                   context={'coords': coords})
        cache.set('response', response)
    # response = PlaceSerializer(requests.get(url).json()['results'],
    #                            many=True,
    #                            context={'coords': coords})
    # json_file = open('places_api/fixtures/dev/api_response.json')
    # response_json = json.load(json_file)
    # response = PlaceSerializer(response_json,
    #                            many=True,
    #                            context={'coords': coords})
    print(url)
    return response.data
