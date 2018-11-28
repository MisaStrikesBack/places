# -*- coding: utf-8 -*-
"""
project constants
"""
from os import environ

API_KEY = environ.get('API_KEY')
API_URL = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
API_REQUEST = '{0}key={1}&'.format(API_URL, API_KEY)

ORDER_VALUES = {
    'newer': '-creation_date',
    'older': 'creation_date',
    'better': '-rating',
    'worst': 'rating'}


DISTANCE_VALUES = {
    'near': False,
    'far': True}
