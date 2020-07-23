from .models import User
from rest_framework.response import Response
import os

import base64
from datetime import datetime, timedelta
import json

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
import jwt

def decode_jwt(jwt_value):
    """
    :type jwt_value: str
    """
    try:
        headers_enc, payload_enc, verify_signature = jwt_value.split(".")
    except ValueError:
        raise jwt.InvalidTokenError()

    payload_enc += '=' * (-len(payload_enc) % 4)  # add padding
    payload = json.loads(base64.b64decode(payload_enc).decode("utf-8"))

    algorithms = getattr(settings, 'JWT_JWS_ALGORITHMS', ['HS256', 'RS256'])
    

    decoded = jwt.decode(jwt_value, os.environ['SECRET_KEY'], algorithms=algorithms)
    return decoded



class UserActionMiddleware:
    """From django docs"""
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.



        response = self.get_response(request)
         # Code to be executed for each request/response after
        # the view is called.
        path = request.get_full_path().split('/') #list with words from url path

        token = request.META.get('HTTP_AUTHORIZATION', '')

        if token:
            
            token = token[7:]
            data = decode_jwt(token)
            user_id = data['user_id']
            user = User.objects.get(id=user_id)
            user.last_action_time = datetime.now()
            user.save()

        if 'token' in path:
            if 'refresh' in path:
                token = request.POST['refresh']
                token = token[7:]
                data = decode_jwt(token)
                user_id = data['user_id']
                user = User.objects.get(id=user_id)
                user.last_login = datetime.now()
            else:
                username = request.POST.get('email')
                password = request.POST.get('password')
                user = User.objects.get(email=username)
                user.last_login = datetime.now()
            user.save()

        return response