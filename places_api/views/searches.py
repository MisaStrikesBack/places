# -*- coding: utf-8 -*-
"""
Searches views
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from places_api.serializers import SearchesSerializer
from places_api.utils.gateway import get_info


class SearchesViewSet(APIView):
    serializer_class = SearchesSerializer
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        """
        Get custom method
        """
        # validating the query params
        search_data = SearchesSerializer(data=self.request.query_params)
        search_data.is_valid(raise_exception=True)
        # getting the maps info
        response = get_info(search_data.validated_data,
                            (self.request.query_params['lat'],
                             self.request.query_params['long']))
        return Response(response)
