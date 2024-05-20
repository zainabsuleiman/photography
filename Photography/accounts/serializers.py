from django.urls import path, include
from django.contrib.auth.models import User, Group
from django.contrib import admin
admin.autodiscover()
from  .models import *
from rest_framework import generics, permissions, serializers
from django.contrib.auth.hashers import make_password, check_password
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', "names","phone","role")
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'
class UserSerializers(serializers.Serializer):
    names = serializers.CharField(max_length=200)
    username = serializers.CharField(max_length=200)
    phone = serializers.CharField(max_length=200)
    email = serializers.EmailField()
    role= serializers.IntegerField()
    def createUser(self):
        users = User()
        users.names = self.validated_data.get('names')
        users.username = self.validated_data.get('username')
        users.phone = self.validated_data.get('phone')
        users.email = self.validated_data.get('email')
        users.is_defaultPassword = True
        users.password = make_password('p@ssw@rd')
        users.role = Role.objects.get(pk=self.validated_data.get('role'))
        users.save()
        return users