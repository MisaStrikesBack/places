# -*- coding: utf-8 -*-
"""
Tests for favorite services
"""
from django.urls import reverse
from django.test import TestCase

from rest_framework.test import APIClient

from places_api.models import Favorite


class TestFavoriteDeleteService(TestCase):
    """
    Test favorites delete service
    """
    fixtures = [
        'dev/users',
        "dev/favorites"
    ]
    maxDiff = None

    def setUp(self):
        """
        Test case setup
        """
        self.user = APIClient()
        self.services = {
            'delete': reverse('api:favorites-detail', kwargs={'pk': 2})
        }

    def test_delete(self):
        """
        Test favorite delete service
        """
        # unauthenticated request
        response = self.user.get(self.services['delete'])
        self.assertEqual(response.status_code, 401)
        # user authentication
        self.user.login(
            username='customer@test.com', password='123porPlaces')
        original_favorites = Favorite.objects.filter(user_id=1).count()
        response = self.user.delete(self.services['delete'])
        self.assertEqual(response.status_code, 204)
        # checking the total amount of user favorites
        self.assertEqual(original_favorites - 1,
                         Favorite.objects.filter(user_id=1).count())
        # retrieving favorite with pk = 2
        self.assertFalse(Favorite.objects.filter(pk=2))

    def test_delete_validation(self):
        """
        Test delete service validations
        """
        # user authentication
        self.user.login(
            username='customer@test.com', password='123porPlaces')
        # triying to delete another user favorite
        response = self.user.delete(self.services['delete'].replace('2', '4'))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {
            'detail': 'Not found.'
        })
