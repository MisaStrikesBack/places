# -*- coding: utf-8 -*-
"""
project constants
"""
from os import environ

api_key = environ.get('API_KEY')
api_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
api_request = '{0}key={1}&'.format(api_url, api_key)
