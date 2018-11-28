# -*- coding: utf-8 -*-
"""
Favorite model
"""
from geopy import distance

from django.db import models
from django.contrib.auth.models import User


class Favorite(models.Model):
    """
    Favorite model
    """
    user = models.ForeignKey(User, related_name='favorites',
                             on_delete=models.CASCADE)
    api_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    place_id = models.CharField(max_length=100)
    rating = models.DecimalField(max_digits=2, decimal_places=1, null=True,
                                 blank=True)
    vicinity = models.CharField(max_length=150)
    lat = models.DecimalField(max_digits=10,
                              decimal_places=7)
    long = models.DecimalField(max_digits=10,
                               decimal_places=7)
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('api_id', 'user')

    def get_distance(self, coords):
        """
        Returns the distance between the object and any given coordinates
        """
        return distance.distance(coords, (self.lat, self.long)).m
