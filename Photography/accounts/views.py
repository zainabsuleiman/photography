from django.shortcuts import render
from .models import *
# Create your views here.

from django.http import JsonResponse
from django.http import Http404
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate , login
from rest_framework import status
from .serializers import *
from .models import *
from django.contrib.auth.hashers import make_password, check_password
import json
import requests
from rest_framework import generics, permissions
from rest_framework.response import Response
from .serializers import UserSerializer
from django.contrib.auth import login
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from rest_framework import permissions
from oauth2_provider.contrib.rest_framework.authentication import OAuth2Authentication