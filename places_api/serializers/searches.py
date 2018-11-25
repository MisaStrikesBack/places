# -*- coding: utf-8 -*-
"""
Searches serializers
"""
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
