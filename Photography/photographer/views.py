from django.shortcuts import render ,redirect
from django.http import JsonResponse
from django.http import Http404
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate , login
from rest_framework import status
from .models import *
from accounts.models import *
from django.contrib.auth.hashers import make_password, check_password
import json
import requests
import math
import random
from rest_framework import generics, permissions
from django.contrib.auth import login
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from rest_framework import permissions
from oauth2_provider.contrib.rest_framework.authentication import OAuth2Authentication

from django.views.decorators.http import require_http_methods
from django.http import HttpResponse

from photographer.serializer.serializers import ActivitySerializer,PhotographerSerializer, UserProfileSerializer

from client.serializer.serializers import AppointmentSerializer
from client.models import Appointment,Appointment_manager

# Create your views here.

#create account for Phtotographer
@api_view(['POST'])
@permission_classes([AllowAny])
def CreateAccount(request):
    photographer = Photographer()
    photographer.firstName=request.data['firstName']
    photographer.lastName=request.data['lastName']
    photographer.district = request.data['district']
    photographer.age= request.data['age']
    photographer.phone=request.data['phone']
    if bool(request.FILES.get('photo')):
        photographer.photo=request.FILES.get('photo')
    photographer.province= request.data['province']
    photographer.sector=request.data['sector']
    photographer.streetNumber=request.data['streetNumber']
    photographer.years_experience=request.data['years_experience']
    photographer.save()
    users = User()
    users.email= request.data['email']
    users.username=request.data['username']
    users.password=make_password(request.data['password'])  
    users.names=photographer.firstName+photographer.lastName
    users.ref_nbr=photographer.pk
    users.phone=photographer.phone
    users.role= Role.objects.get(type_name='photographer')
    users.is_active=False
    users.save()
    return Response("msg:created", status=status.HTTP_200_OK)




#notificatio of approval
def ApproveNotification(phone ,name,date_submitted):
    token='eyJhbGciOiJub25lIn0.eyJpZCI6MzczLCJyZXZva2VkX3Rva2VuX2NvdW50IjowfQ.'
    headers = {'Authorization': 'Bearer ' + token}
    s = ' Dear {} your Accaunt created on {} has been Approved , now you can start your activity in the system thanks'.format(name,date_submitted)  
    data = {'to' : phone, 'text' : s, 'sender' : 'My Art Studio'}
    url = 'https://api.pindo.io/v1/sms/'
    response = requests.post(url, json=data, headers=headers)
    print(response)
    print(response.json())
    return Response(response)


#user profile
class UserProfileView(APIView):
  authentication_classes = [OAuth2Authentication]
  permission_classes = [IsAuthenticated]
  def get(self, request, format=None):
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)




#details of photographer
@api_view(['GET'])
@authentication_classes([OAuth2Authentication])
@permission_classes([IsAuthenticated])
def Phototgrapherdetails(request,pk):
  photographer =Photographer.objects.get(pk=pk)
  serializer = PhotographerSerializer(photographer,many=False)
  return Response(serializer.data,status=status.HTTP_200_OK)




#Approve account of photographer
@api_view(['PUT'])
@authentication_classes([OAuth2Authentication])
@permission_classes([IsAuthenticated])
def Approve_Photographer(request,pk):
    users = User.objects.get(ref_nbr=pk)
    users.is_active=True
    users.save()
    name = users.first_name
    phone=users.phone
    date=users.created_at
    # ApproveNotification(phone,name,date)
    return Response("msg:User Approved", status=status.HTTP_200_OK)


#Add activity of photographer
@api_view(['POST'])
@authentication_classes([OAuth2Authentication])
@permission_classes([IsAuthenticated])
def createActivity(request,pk):
    activity = Activity()
    activity.name=request.data['name']
    activity.price=request.data['price']
    activity.activity_type=request.data['activity_type']
    activity.photographer = Photographer.objects.get(pk=pk)
    activity.save()
    return Response("Activity Saved Successfuly", status=status.HTTP_200_OK)


#update activity by id
@api_view(['PUT'])
@authentication_classes([OAuth2Authentication])
@permission_classes([IsAuthenticated])
def changeActivityStatus(request,pk):

    activity=Activity.objects.get(pk=pk)
    if(activity==None):
        return Response("Activity Not Found", status=status.HTTP_404_NOT_FOUND)
    activity.canBeRequested= not activity.canBeRequested
    activity.save()
    serializer=ActivitySerializer(activity)
    return Response(serializer.data, status=status.HTTP_200_OK)


#searching activity for certain photographer
@api_view(['GET'])
@authentication_classes([OAuth2Authentication])
@permission_classes([IsAuthenticated])
def activityList(request,pk):

    photographer=Photographer.objects.get(pk=pk)
    if(photographer==None):
        return Response("Photographer Not Found", status=status.HTTP_404_NOT_FOUND)
    activities=Activity.objects.filter(photographer=photographer)
    serializer=ActivitySerializer(activities,many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


#update profile for photographer
@api_view(['PUT'])
@permission_classes([AllowAny])
def updateProfile(request,pk):
    photographer = Photographer.objects.get(pk=pk)
    if(photographer==None):
        return Response("Photographer with "+pk+" Not Founnd", status=status.HTTP_404_NOT_FOUND)
    photographer.firstName=request.data['firstName']
    photographer.lastName=request.data['lastName']
    photographer.district = request.data['district']
    photographer.age= request.data['age']
    photographer.phone=request.data['phone']
    if bool(request.FILES.get('photo')):
        photographer.photo=request.FILES.get('photo')
    photographer.province= request.data['province']
    photographer.sector=request.data['sector']
    photographer.streetNumber=request.data['streetNumber']
    photographer.years_experience=request.data['years_experience']
    photographer.save()
    serializer=PhotographerSerializer(photographer)
    return Response(serializer.data, status=status.HTTP_200_OK)

#list of photographer
@api_view(['GET'])
@authentication_classes([OAuth2Authentication])
@permission_classes([IsAuthenticated])
def photographerList(request):
    photographers=Photographer.objects.all()
    serializer=PhotographerSerializer(photographers,many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


#details of photographer
@api_view(['GET'])
@authentication_classes([OAuth2Authentication])
@permission_classes([IsAuthenticated])
def photographerDetails(request,pk):
    photographers=Photographer.objects.get(pk=pk)
    serializer=PhotographerSerializer(photographers,many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)


# ###############################################################
# Listing Photographer Appointment
@api_view(['GET'])
@authentication_classes([OAuth2Authentication])
@permission_classes([IsAuthenticated])
def photographerAppointments(request,pk):

    appointments=Appointment.objects.filter(photographer=pk,status='SUBMITTED')
    serializer=AppointmentSerializer(appointments,many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
#appointment approval notification
def ApproveappointmentNotification(phone ,name,date_submitted):
    token='eyJhbGciOiJub25lIn0.eyJpZCI6MzczLCJyZXZva2VkX3Rva2VuX2NvdW50IjowfQ.'
    headers = {'Authorization': 'Bearer ' + token}
    s = ' Dear {} your Appointment with {} has been Approved , now you can log into the system for Advance payment'.format(name,date_submitted)  
    data = {'to' : phone, 'text' : s, 'sender' : 'My Art Studio'}
    url = 'https://api.pindo.io/v1/sms/'
    response = requests.post(url, json=data, headers=headers)
    print(response)
    print(response.json())
    return Response(response)
#halfpaid appointmentlist
@api_view(['GET'])
@authentication_classes([OAuth2Authentication])
@permission_classes([IsAuthenticated])
def photographerAppointments_half(request,pk):

    appointments=Appointment.objects.filter(photographer=pk,payment_status='HALF PAID')
    serializer=AppointmentSerializer(appointments,many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
# Photographer Approve Apointment
@api_view(['POST'])
@authentication_classes([OAuth2Authentication])
@permission_classes([IsAuthenticated])
def approve_appointment(request,pk):
    appointment=Appointment.objects.get(pk=pk)
    if(appointment==None):
        return Response("Appointment Not Found", status=status.HTTP_404_NOT_FOUND)

    pre_requisite_amount=request.data['pre_requisite_amount']    
    # checking if Pre-Requesite Amount does not exceed 50 %
    if(float(appointment.appointment_total_price) < (float(pre_requisite_amount)*0.5)):
         return Response("Pre-Requesite Amount exceeded 50 percent of the Appoitment Price", status=status.HTTP_400_BAD_REQUEST)

    appointment_manager=Appointment_manager()
    appointment_manager.payment=request.data['pre_requisite_amount'] 
    appointment_manager.status='NOT PAID'
    appointment_manager.comment=request.data['comment']
    appointment_manager.appointment=appointment
    appointment_manager.save()
    appointment.status='APPROVED'
    # name = appointment.client.firstName
    # phone = appointment.client.phone
    # date =  appointment.photographer_name
    appointment.save()
    #ApproveappointmentNotification(name,phone,date)
    return Response(appointment)
    
    