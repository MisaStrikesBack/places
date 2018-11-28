# -*- coding: utf-8 -*-
"""
Searches serializers
"""
from geopy import distance

from rest_framework import serializers

from places_api.serializers import FavoritesBaseSerializer
from places_api.serializers.base_query import BaseQuerySerializer


class SearchQuerySerializer(BaseQuerySerializer):
    """
    searches serializer class
    """
    keyword = serializers.CharField(max_length=100, required=False)
    radius = serializers.IntegerField(min_value=1, required=False)
    next_page_token = serializers.CharField(max_length=300, required=False)


class SearchResultsSerializer(FavoritesBaseSerializer):
    """
    Search results serializer
    """
    api_id = serializers.CharField(source='id', max_length=50)
    lat = serializers.DecimalField(source='geometry.location.lat',
                                   max_digits=10,
                                   decimal_places=7)
    long = serializers.DecimalField(source='geometry.location.lng',
                                    max_digits=10,
                                    decimal_places=7)
    distance = serializers.SerializerMethodField()

    class Meta(FavoritesBaseSerializer.Meta):
        fields = FavoritesBaseSerializer.Meta.fields + ['distance']

    def get_distance(self, obj):
        """
        Calculating distance
        """
        location = obj['geometry']['location']
        return distance.distance((self.context['coords']),
                                 (location['lat'], location['lng'])).m


class ApiResponseSerializer(serializers.Serializer):
    """
    Google api response serializer
    """
    next_page_token = serializers.CharField(max_length=300, required=False)
    places = SearchResultsSerializer(source='results', many=True,
                                     read_only=True)
