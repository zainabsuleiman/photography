from django.urls import path, include
from django.contrib.auth.models import User, Group
from django.contrib import admin
admin.autodiscover()
from photographer.models import Photographer,Activity
from rest_framework import generics, permissions, serializers
from django.contrib.auth.hashers import make_password, check_password
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
class PhotographerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photographer
        fields = '__all__'

class CreateAccount(serializers.Serializer):
   firstName = serializers.CharField(max_length=200)
   lastName = serializers.CharField(max_length=200)
   phone = serializers.CharField(max_length=200)
   age = serializers.IntegerField()
   photo = serializers.ImageField()
   province = serializers.CharField(max_length=200)
   district = serializers.CharField(max_length=200)
   sector = serializers.CharField(max_length=200)
   streetNumber = serializers.CharField(max_length=200)
   years_experience = serializers.IntegerField()
   username = serializers.CharField(max_length=200)
   email = serializers.EmailField()
   names = serializers.CharField(max_length=200)
   password = serializers.CharField(max_length=200)
   phone = serializers.CharField(max_length=200)
   ref_nbr = serializers.CharField(max_length=200)
   def create(self):
       photographer = Photographer()
       photographer.firstName = self.validated_data.get('firstName')
       photographer.lastName= self.validated_data.get('lastName')
       photographer.phone=self.validated_data.get('phone')
       photographer.age  =self.validated_data.get('age')
       photographer.photo=self.validated_data.get('photo')
       photographer.province=self.validated_data.get('province')
       photographer.district=self.validated_data.get('district')
       photographer.sector=self.validated_data.get('sector')
       photographer.streetNumber=self.validated_data.get('streetNumber')
       photographer.years_experience=self.validated_data.get('year_experience')
       photographer.save()
       users = User()
       
       return photographer


#user profile serializer
class UserProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'email', 'username','role','is_active','is_admin','ref_nbr']

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'