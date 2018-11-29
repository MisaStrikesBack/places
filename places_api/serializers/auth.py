# -*- coding: utf-8 -*-
"""
Authentication serializers
"""
from django.contrib.auth.models import User

from rest_framework import serializers

from places_api.error_messages import (
    INCLUDE_EMAIL, SHORTER_EMAIL, VALID_EMAIL, SUBMIT_PASSWORD, VALID_PASSWORD,
    EMAIL_IN_USE, UNMATCHING_PASSWORDS)


class PasswordsBaseSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6, max_length=20,
                                     style={'input_type': 'password'},
                                     write_only=True)
    confirm_password = serializers.CharField(min_length=6, max_length=20,
                                             style={'input_type': 'password'},
                                             write_only=True)

    def validate(self, data):
        if (data['password'] == data['confirm_password']):
            return data
        raise serializers.ValidationError(UNMATCHING_PASSWORDS)


class SignInSerializer(serializers.Serializer):
    """
    Sign In serializer
    """
    email = serializers.EmailField(
        max_length=60,
        error_messages={
            'required': INCLUDE_EMAIL,
            'blank': INCLUDE_EMAIL,
            'max_length': SHORTER_EMAIL,
            'invalid': VALID_EMAIL
        }
    )
    password = serializers.CharField(
        min_length=4,
        max_length=40,
        error_messages={
            'required': SUBMIT_PASSWORD,
            'blank': VALID_PASSWORD
        },
        style={'input_type': 'password'}
    )


class SignUpSerializer(PasswordsBaseSerializer):
    """
    Sign Up serializer
    """
    first_name = serializers.CharField(max_length=50)
    email = serializers.EmailField(max_length=50)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password',
                  'confirm_password')
        extra_kwargs = {'email': {"allow_null": False}}

    def validate_email(self, value):
        """
        email validator
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(EMAIL_IN_USE)
        return value

    def create(self, validated_data):
        """
        Create method for SignUp Serializer
        """
        # creating the new user
        new_user = User(
            username=validated_data['email'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            is_active=True)

        new_user.set_password(validated_data['password'])
        new_user.save()
        return new_user


class UpdatePasswordSerializer(PasswordsBaseSerializer):
    """
    ResetPasswordSerializer class
    """
    current_password = serializers.CharField(min_length=6, max_length=20,
                                             style={'input_type': 'password'})
