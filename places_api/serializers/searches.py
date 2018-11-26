# -*- coding: utf-8 -*-
"""
Searches serializers
"""
from geopy import distance

from rest_framework import serializers


class SearchesSerializer(serializers.Serializer):
    """
    searches serializer class
    """
    lat = serializers.DecimalField(max_digits=10,
                                   decimal_places=7)
    long = serializers.DecimalField(max_digits=10,
                                    decimal_places=7)
    keyword = serializers.CharField(max_length=100,
                                    required=False)
    radius = serializers.IntegerField(min_value=1,
                                      required=False)
    order = serializers.CharField(max_length=40,
                                  required=False)


class PlaceSerializer(serializers.Serializer):
    """
    Google api response serializer
    """
    id = serializers.CharField(max_length=100)
    name = serializers.CharField(max_length=100)
    place_id = serializers.CharField(max_length=100)
    rating = serializers.DecimalField(max_digits=2, decimal_places=1,
                                      required=False)
    vicinity = serializers.CharField(max_length=150)
    location = serializers.SerializerMethodField()
    distance = serializers.SerializerMethodField()

    def get_location(self, obj):
        return obj['geometry']['location']

    def get_distance(self, obj):
        location = obj['geometry']['location']
        return distance.distance((self.context['coords']),
                                 (location['lat'], location['lng'])).m
