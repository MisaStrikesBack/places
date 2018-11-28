# -*- coding: utf-8 -*-
"""
Favorites views
"""
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from places_api.models import Favorite
from places_api.serializers import (
    FavoritesModelSerializer, FavoritesQuerySerializer)
from places_api.constants import ORDER_VALUES, DISTANCE_VALUES


class FavoritesViewSet(mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.CreateModelMixin,
                       mixins.DestroyModelMixin,
                       viewsets.GenericViewSet):
    """
    Favorites view set
    """
    serializer_class = FavoritesModelSerializer
    permission_classes = (IsAuthenticated, )

    def check_params(self):
        list_params = FavoritesQuerySerializer(data=self.request.query_params)
        list_params.is_valid(raise_exception=True)
        return list_params.validated_data

    def get_queryset(self):
        """
        only user favorites are part of the queryset
        """
        qs = Favorite.objects.filter(user=self.request.user)
        data = self.check_params()
        order_value = data.get('order')
        if order_value in ORDER_VALUES.keys():
            return qs.order_by(ORDER_VALUES[order_value])
        elif order_value in DISTANCE_VALUES.keys():
            dist_aux = []
            coord = (data['lat'], data['long'])
            for favorite in qs:
                dist_aux.append((favorite.get_distance((coord)), favorite.pk))
            dist_aux = (
                [x[1] for x in sorted(
                    dist_aux, key=lambda dist: dist[0],
                    reverse=DISTANCE_VALUES[order_value])])
            clauses = (
                ' '.join(['WHEN id=%s THEN %s' % (pk, i)
                         for i, pk in enumerate(dist_aux)]))
            ordering = 'CASE %s END' % clauses
            return qs.filter(pk__in=dist_aux).extra(
                select={'ordering': ordering}, order_by=('ordering',))
        return qs
