# -*- coding: utf-8 -*-
"""
Searches serializers
"""
from rest_framework import serializers
from places_api.error_messages import REQUIRED_QUERY_PARAM


class LatLngSerializer(serializers.Serializer):
    """
    Base lat lng serializer
    """
    lat = serializers.DecimalField(max_digits=10, decimal_places=7,
                                   error_messages={
                                       'required': REQUIRED_QUERY_PARAM})
    long = serializers.DecimalField(max_digits=10, decimal_places=7,
                                    error_messages={
                                       'required': REQUIRED_QUERY_PARAM})


class BaseQuerySerializer(LatLngSerializer):
    """
    Common latitude longitude serializer fields
    """
    order = serializers.CharField(max_length=40, required=False)
