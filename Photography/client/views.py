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
from .serializer.serializers import *
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
from client.serializer.serializers import AppointmentSerializer,AppointmentManagerSerializer
from rest_framework.parsers import FileUploadParser
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

 

# Create your views here.
#create client account
@api_view(['POST'])
@authentication_classes([OAuth2Authentication])
@permission_classes([AllowAny])
def CreateAccount(request):
 serializer = CreateClientSerializer(data=request.data)
 client=None
 if serializer.is_valid():
       client = serializer.create()
       serial = ClientSerializer(client)
       return Response(serial.data)
 else:
        return Response({'msg':serializer.errors}) 
class UserProfileView(APIView):
  authentication_classes = [OAuth2Authentication]
  permission_classes = [IsAuthenticated]
  def get(self, request, format=None):
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)
#update profile
#users
@api_view(['GET'])
@authentication_classes([OAuth2Authentication])
@permission_classes([IsAdminUser])
def Userslist(request):
    users=User.objects.all()
    if(users==None):
      return Response("Users List Not Found", status=status.HTTP_404_NOT_FOUND)
    serializer=UserProfileSerializer(users,many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
#list of clients
@api_view(['GET'])
@authentication_classes([OAuth2Authentication])
@permission_classes([IsAuthenticated])
def listofClient(request):
  client =Client.objects.all()
  serializer = ClientSerializer(client,many=True)
  return Response(serializer.data,status=status.HTTP_200_OK)



#details of client
@api_view(['GET'])
@authentication_classes([OAuth2Authentication])
@permission_classes([IsAdminUser])
def Clientdetails(request,pk):
  client =Client.objects.get(pk=pk)
  serializer = ClientSerializer(client,many=False)
  return Response(serializer.data,status=status.HTTP_200_OK)



#make appointment
@api_view(['POST'])
@authentication_classes([OAuth2Authentication])
@permission_classes([IsAuthenticated])
def createAppointment(request,pk):
    client=Client.objects.get(pk=request.user.ref_nbr)
    photographer=Photographer.objects.get(pk=pk)
    if(photographer==None):
      return Response("Photographer with "+pk+" Not Found", status=status.HTTP_404_NOT_FOUND)
    
    appointment=Appointment()
    appointment.location=request.data['location']
    appointment.hours_min=request.data['hours_min']
    appointment.description=request.data['description']
    appointment.status='PENDING'
    appointment.payment_status='NOT PAID'
    appointment.photographer_name =photographer.firstName +' '+ photographer.lastName
    appointment.client=client
    appointment.photographer=photographer
    appointment.save()

    serializer=AppointmentSerializer(appointment,many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)


#appointment details
@api_view(['GET'])
@authentication_classes([OAuth2Authentication])
@permission_classes([IsAuthenticated])
def appointmentDetails(request,pk):
    appointment=Appointment.objects.get(pk=pk)
    if(appointment==None):
      return Response("Appointment with "+pk+" Not Found", status=status.HTTP_404_NOT_FOUND)
    serializer=AppointmentSerializer(appointment,many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)

#######################################################################
# API For Assigning Activity to Appointment
@api_view(['POST'])
@authentication_classes([OAuth2Authentication])
@permission_classes([IsAuthenticated])
def assignAppointmentActivity(request,pk):
   # print("+++++"+request.data['activities'])
    appointment=Appointment.objects.get(pk=pk)
    if(appointment==None):
      return Response("Appointment with "+pk+" Not Found", status=status.HTTP_404_NOT_FOUND)
    else:
        activities=request.data['activities']
       # print("*****"+activities)
        activity_of_list=activities.split("#")
        print(activity_of_list)
        total=0.0
        for a in activity_of_list:
            actitity=Activity.objects.get(pk=a)
            app_activity=AppointmentActivity()
            app_activity.activity=actitity
            app_activity.appointment=appointment
            app_activity.save()
            total=total+actitity.price
        appointment.status='SUBMITTED'    
        appointment.appointment_total_price=str(total)
        appointment.save()

        print(app_activity)
        return Response("Appointment Activities Assigned Successfuly", status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([OAuth2Authentication])
@permission_classes([IsAuthenticated])
def listClientAppointments(request,pk):
    client=Client.objects.get(pk=request.user.ref_nbr)
    appointments=Appointment.objects.filter(photographer=pk,client=client)
    serializer=AppointmentSerializer(appointments,many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)  
#approved appointment
@api_view(['GET'])
@authentication_classes([OAuth2Authentication])
@permission_classes([IsAuthenticated])
def listClientAppointments_approved(request,pk):
    appointments=Appointment_manager.objects.filter(appointment=pk)
    serializer=AppointmentManagerSerializer(appointments,many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)  

#list of all appointment based on client
@api_view(['GET'])
@authentication_classes([OAuth2Authentication])
@permission_classes([IsAuthenticated])
def ClientAppointments(request):
    client=Client.objects.get(pk=request.user.ref_nbr)
    appointments=Appointment.objects.filter(client=client)
    serializer=AppointmentSerializer(appointments,many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)   
def process_payment(name,email,amount,phone):
     #auth_token= env('FLUTTER_WAVE')
     hed = {'Authorization': 'Bearer ' + 'FLWSECK_TEST-83f1f44f7960a45b467de7bb57e1c9d2-X','Content-Type': 'application/json',}
     data = {
                "tx_ref":''+str(math.floor(1000000 + random.random()*9000000)),
                "amount":amount,
                "currency":"RWF",
                "redirect_url":"http://localhost:3000/#/dashboard/industry/",
                "payment_options":"mobilemoney",
                "customer":{
                    "email":email,
                    "phonenumber":phone,
                    "name":name
                },
                "customizations":{
                    "title":"My Art studio System",
                    "description":"Pay",
                    "logo":""
                }
                }
     url = 'https://api.flutterwave.com/v3/payments'
     response = requests.post(url, json=data, headers=hed)
     response=response.json()
     print('***')
     print(response)
    #  if response['status'] == "success":
    #            return response
     link=response['data']['link']
     return link 
@api_view(['POST'])
@authentication_classes([OAuth2Authentication])
@permission_classes([IsAuthenticated])
def CreatePlan(request, pk):
    manage = Appointment_manager.objects.get(appointment=pk)
    app = Appointment.objects.get(id=pk)
    plan = Plan()
    plan.names = request.data['names']
    plan.email = request.data['email']
    plan.phone = request.data['phone']
    plan.amount=manage.payment
    plan.appointment = Appointment.objects.get(id=pk)
    app.payment_status = 'HALF PAID'
    app.save()
    plan.save()
    name =plan.names
    email = plan.email
    amount = plan.amount
    phone = plan.phone 
    return  Response({"link": process_payment(name,email,amount,phone)})


class FilesUploadAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    permission_classes = (permissions.AllowAny,)

    def get(self, request,pk, format=None, *args, **kwargs):
        file = Appointments_uploads.objects.filter(appointment__pk=pk)
        serializer = FileSerializer(file, many=True)
        
        return Response(serializer.data)


    def post(self, request,pk, format=None):
        serializer = FileListSerializer(data=request.data)
        app=None
        files_list = request.FILES.getlist('file')
        if serializer.is_valid():
            for item in files_list:
                upload=Appointments_uploads()
                upload.photo_result=item
                upload.appointment=Appointment.objects.get(id=pk)
                upload.save()
                app=upload.appointment
            app.status='FINAL_PAYMENT'
            app.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#viewing uploads
@api_view(['GET'])
@authentication_classes([OAuth2Authentication])
@permission_classes([IsAuthenticated])
def Uploads(request, pk):
     app = Appointments_uploads.objects.filter(appointment=pk)
     serializer = Appointment_uploadsSerializer(app, many=True)
     return Response(serializer.data)


 