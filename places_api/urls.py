# -*- coding: utf-8 -*-
"""
places_api urls
"""
from django.urls import path, include

from places_api.views import (
    SignOutView, SignInView, SignUpView, UpdatePasswordView)

app_name = "places_api"

auth_patterns = ([
    path('signout/', SignOutView.as_view(), name='signout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('update/', UpdatePasswordView.as_view(), name='update'),
], 'auth')

urlpatterns = [
    path('auth/', include(auth_patterns)),
]
