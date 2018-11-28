# -*- coding: utf-8 -*-
"""
places_api viewset router
"""
from django.urls import path
from rest_framework.routers import SimpleRouter

from places_api.views import FavoritesViewSet, SearchViewSet

api_router = SimpleRouter()

api_router.register(
    r'favorites', FavoritesViewSet, base_name='favorites')

# non mixin views
api_router.urls.append(
    path('search/', SearchViewSet.as_view(), name='search'),
)
