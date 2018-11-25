# -*- coding: utf-8 -*-
"""
favorites serializers
"""
from rest_framework import serializers

from places_api.models import Favorite


class FavoritesSerializer(serializers.ModelSerializer):
    """
    Favorite standard serializer
    """
    class Meta:
        model = Favorite
        fields = ['pk', 'place_id']
