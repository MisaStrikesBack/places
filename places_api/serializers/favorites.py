# -*- coding: utf-8 -*-
"""
favorites serializers
"""
from rest_framework import serializers

from places_api.models import Favorite
from places_api.error_messages import INVALID_USER
from places_api.serializers.base_query import BaseQuerySerializer


class FavoritesQuerySerializer(BaseQuerySerializer):
    """
    Favorites query param serializer
    """

    def validate_order(self, value):
        if value not in ['newer', 'older', 'near', 'far', 'better', 'worst']:
            return None
        return value


class FavoritesBaseSerializer(serializers.ModelSerializer):
    """
    Favorite standard serializer
    """
    class Meta:
        model = Favorite
        fields = ['pk', 'api_id', 'name', 'place_id', 'rating',
                  'vicinity', 'lat', 'long']


class FavoritesModelSerializer(FavoritesBaseSerializer):
    """
    Full model serializer
    """
    distance = serializers.SerializerMethodField(read_only=True)

    class Meta(FavoritesBaseSerializer.Meta):
        fields = FavoritesBaseSerializer.Meta.fields + ['user',
                                                        'creation_date',
                                                        'distance']
        extra_kwargs = {'user': {"write_only": True}}

    def validate_user(self, value):
        """
        Validating the user id because a user can only create favorites for
        himself
        """
        if value.id != self.context['request'].user.id:
            raise serializers.ValidationError(INVALID_USER)
        return value

    def get_distance(self, obj):
        """
        Returning the model method get_distance
        """
        params = self.context['request'].query_params
        return obj.get_distance((params['lat'], params['long']))
