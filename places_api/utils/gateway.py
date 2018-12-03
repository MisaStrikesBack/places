# -*- coding: utf-8 -*-
"""
External api consumption file
"""
import requests

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
    # setting order
    url = set_order(url, data)
    # setting ordering
    url = set_keyword(url, data)
    page_index = data['page'] if data.get('page') else 1
    if url != cache.get('url'):
        print('new url')
        # clearing cache to flush all possible pages
        cache.clear()
        # set new url
        cache.set('url', url)
        # getting new response
        response = requests.get(url)
        # setting the first page, the pages number, and the used tokens list
        cache.set('page_1', response)
        cache.set('pages', 1)
        cache.set('tokens', [])
    # checking if next_page token and nex_page token not repeated
    elif (data.get('next_page') and
            data['next_page'] not in cache.get('tokens')):
        print('add page')
        # setting the pagination url
        token_url = '{0}pagetoken={1}'.format(url, data['next_page'])
        # requseting new page
        response = requests.get(token_url)
        # assesing request response
        if response and response.json()['status'] == 'OK':
            # storing the token string
            cache.set('tokens', cache.get('tokens') + [data['next_page']])
            # updating the number of pages
            page_index = cache.get('pages') + 1
            # storing the new page in cache
            cache.set("page_{0}".format(page_index),
                      response)
            # storing new number of pages in cache
            cache.set('pages', page_index)

    api_response = ApiResponseSerializer(
        cache.get("page_{0}".format(page_index)).json(),
        context={
          'coords': coords,
          'total_pages': cache.get('pages'),
          'current_page': page_index})
    return api_response.data
