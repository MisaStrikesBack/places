# -*- coding: utf-8 -*-
"""
Favorites views
"""
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from places_api.models import Favorite
from places_api.serializers import FavoritesSerializer


class FavoritesViewSet(mixins.ListModelMixin,
                       viewsets.GenericViewSet):
    """
    Favorites view set
    """
    serializer_class = FavoritesSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        """
        only user favorites are part of the queryset
        """
        return Favorite.objects.filter(user=self.request.user)
