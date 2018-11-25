# -*- coding: utf-8 -*-
"""
Favorite model
"""
from django.db import models
from django.contrib.auth.models import User


class Favorite(models.Model):
    """
    Favorite model
    """
    place_id = models.CharField(max_length=50)
    user = models.ForeignKey(User,
                             related_name='favorites',
                             on_delete=models.CASCADE)
