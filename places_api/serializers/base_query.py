# -*- coding: utf-8 -*-
"""
Searches serializers
"""
from rest_framework import serializers


class BaseQuerySerializer(serializers.Serializer):
    """
    Common latitude longitude serializer fields
    """
    lat = serializers.DecimalField(max_digits=10, decimal_places=7)
    long = serializers.DecimalField(max_digits=10, decimal_places=7)
    order = serializers.CharField(max_length=40, required=False)
