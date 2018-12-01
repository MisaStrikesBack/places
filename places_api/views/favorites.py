# -*- coding: utf-8 -*-
"""
Favorites views
"""
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from places_api.models import Favorite
from places_api.serializers import (
    FavoritesModelSerializer, FavoritesQuerySerializer, LatLngSerializer)
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
        serializer = (
            LatLngSerializer if self.action == 'create' else
            FavoritesQuerySerializer)
        list_params = serializer(data=self.request.query_params)
        list_params.is_valid(raise_exception=True)
        return list_params.validated_data

    def get_queryset(self):
        """
        only user favorites are part of the queryset
        """
        # only user favorites are in the queryset
        qs = Favorite.objects.filter(user=self.request.user)
        # if delete, the qs is return with no process
        if self.action == 'destroy':
            return qs
        # validating query params
        data = self.check_params()
        # getting the requested order
        order_value = data.get('order')
        if order_value in ORDER_VALUES.keys():
            # sorting the qs
            return qs.order_by(ORDER_VALUES[order_value])
        # checking id order requires distance measure
        elif order_value in DISTANCE_VALUES.keys():
            dist_aux = []
            # getting the query param lat and long
            coord = (data['lat'], data['long'])
            # getting the raw distance of all favorites
            for favorite in qs:
                # appending a tuple compose by distance and favorite pk
                dist_aux.append((favorite.get_distance((coord)), favorite.pk))
            # this magical list comprehension sorts the dist aux list
            # increasing or decreasing according the order value and returns
            # the distance pk
            dist_aux = (
                [x[1] for x in sorted(
                    dist_aux, key=lambda dist: dist[0],
                    reverse=DISTANCE_VALUES[order_value])])
            # defining sql clauses
            clauses = (
                ' '.join(['WHEN id=%s THEN %s' % (pk, i)
                         for i, pk in enumerate(dist_aux)]))
            ordering = 'CASE %s END' % clauses
            # returning the filtered qs ensuring the order is correct
            return qs.filter(pk__in=dist_aux).extra(
                select={'ordering': ordering}, order_by=('ordering',))
        return qs

    def create(self, request):
        """
        Custom create method
        """
        self.check_params()
        return super().create(request)
