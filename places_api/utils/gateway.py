# -*- coding: utf-8 -*-
"""
External api consumption file
"""
import requests
from django.core.cache import cache

from places_api.constants import api_request

def get_info(data):
    url ="{0}location={1},{2}&radius=1000&".format(
        api_request, data['lat'], data['long'])
    # checking if there is son search value
    if data.get('keyword'):
        url = "{0}keyword={1}".format(url, data['keyword'])
    else:
        url = "{0}type=point_of_interest".format(url)
    response = requests.get(url)
    return response.json()
