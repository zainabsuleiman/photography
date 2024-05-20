from django.urls import path, include
from django.contrib.auth.models import User, Group
from django.contrib import admin
admin.autodiscover()
from client.models import Client
from accounts.models import User,Role
from rest_framework import generics, permissions, serializers
from django.contrib.auth.hashers import make_password, check_password
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from client.models import Appointment,Appointment_manager,Appointments_uploads
class ClientSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Client
        fields = '__all__'
#create account serializer
class CreateClientSerializer(serializers.Serializer):
   firstName = serializers.CharField(max_length=200)
   lastName = serializers.CharField(max_length=200)
   phone = serializers.CharField(max_length=200)
   streetNumber = serializers.CharField(max_length=200)
   district =serializers.CharField(max_length=200)
   province = serializers.CharField(max_length=200)
   cell = serializers.CharField(max_length=200)
   sector = serializers.CharField(max_length=200)
   village = serializers.CharField(max_length=200)
   username = serializers.CharField(max_length=200)
   password = serializers.CharField(max_length=200)
   email = serializers.CharField(max_length=200)
   def create(self):
       client =Client()
       client.firstName=self.validated_data.get('firstName')
       client.lastName=self.validated_data.get('lastName')
       client.phone=self.validated_data.get('phone')
       client.streetNumber=self.validated_data.get('streetNumber')
       client.district=self.validated_data.get('district')
       client.province=self.validated_data.get('province')
       client.cell=self.validated_data.get('cell')
       client.sector=self.validated_data.get('sector')
       client.village=self.validated_data.get('village')
       client.save()
       users=User()
       users.email=self.validated_data.get('email')
       users.username=self.validated_data.get('username')
       users.phone=client.phone
       users.password=make_password(self.validated_data.get('password'))  
       users.names=client.firstName+' '+client.lastName
       users.ref_nbr=client.pk
       users.role=Role.objects.get(type_name='client')
       users.save()
       return client

#user profile 
class UserProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'email', 'username','role','is_active','is_admin','ref_nbr', 'names','phone','created_at','updated_at']


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'
class Appointment_uploadsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointments_uploads
        fields = '__all__'
class AppointmentManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment_manager
        fields = '__all__'
class FileListSerializer(serializers.Serializer) :
    file = serializers.ListField(
                       child=serializers.ImageField( max_length=100000,
                                         allow_empty_file=False,
                                         use_url=False )
                                )
class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointments_uploads  
        fields = '__all__'    