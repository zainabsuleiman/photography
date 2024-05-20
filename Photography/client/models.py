from django.db import models
from photographer.models import Photographer,Activity
from django.core.files import File
from PIL import Image
import datetime

def wrapper(instance, filename):
    new_filename = str(datetime.datetime.now()).split(
        '.')[0]+'_'+str(instance.id).split('-')[0]+'__'+filename
    return 'profilePictures/'+new_filename
def wrapperer(instance, filename):
    new_filename = str(datetime.datetime.now()).split(
        '.')[0]+'_'+str(instance.id).split('-')[0]+'__'+filename
    return 'uploads/'+new_filename
# Create your models here.
class Client(models.Model):
   firstName = models.CharField(max_length=200 )
   lastName = models.CharField(max_length=200)
   phone = models.CharField(max_length=200 ,unique=True )
   streetNumber = models.CharField(max_length=200)
   district =models.CharField(max_length=200)
   province = models.CharField(max_length=200)
   cell = models.CharField(max_length=200)
   sector = models.CharField(max_length=200)
   village = models.CharField(max_length=200)
   def __str__(self):
       return self.phone
   
   class Meta:
     db_table = 'Client'


class Appointment(models.Model):
   location = models.CharField(max_length=200)
   hours_min = models.CharField(max_length=200)
   description = models.CharField(max_length=200)
   photographer = models.ForeignKey(Photographer,null=True,on_delete=models.CASCADE)
   client = models.ForeignKey(Client,null=True,on_delete=models.CASCADE)
   status = models.CharField(max_length=200)
   photographer_name = models.CharField(max_length=50)
   payment_status = models.CharField(max_length=200)
   appointment_total_price=models.CharField(max_length=200)
   class Meta:
     db_table = 'Appointment'

class Appointment_manager(models.Model):
   occurance_date = models.DateTimeField(auto_now_add=True)
   payment = models.FloatField()
   status = models.CharField(max_length=200)
   comment=models.CharField(max_length=1000)
   appointment = models.ForeignKey(Appointment,null=True,on_delete=models.CASCADE)
   class Meta:
     db_table = 'Appointment_manager'


class AppointmentActivity(models.Model):
   appointment = models.ForeignKey(Appointment,null=True,on_delete=models.CASCADE)
   activity = models.ForeignKey(Activity,null=True,on_delete=models.CASCADE)
   deleted = models.BooleanField(default=False)
   class Meta:
     db_table = 'appointment_activity'
class Appointments_uploads(models.Model):
  appointment = models.ForeignKey(Appointment,null=True,on_delete=models.CASCADE)
  photo_result = models.ImageField(upload_to=wrapper, null=True, default=None)

  class Meta:
     db_table = 'Appointment_uploads'
class Plan(models.Model):
    names = models.CharField(max_length=200)
    email= models.EmailField(max_length=200)
    phone = models.CharField(max_length=200)
    amount = models.FloatField()
    appointment = models.ForeignKey(Appointment,null=True,on_delete=models.CASCADE)
    def __str__(self):
        return self.names
    class Meta:
        db_table ='Plan'
class Uploads(models.Model):
  title = models.CharField(max_length=200)
  uploads = models.ImageField(upload_to=wrapperer, null=True, default=None)
  appointment = models.ForeignKey(Appointment,null=True,on_delete=models.CASCADE)
  def __str__(self):
        return self.title
  class Meta:
        db_table ='Uploads'