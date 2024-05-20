from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class Role(models.Model):
    type_name = models.CharField(max_length=200)
    def __str__(self):
        return self.type_name
    class Meta:
     db_table = 'Role'

class User(AbstractUser):
  username = models.CharField(max_length=200,unique=True)
  email = models.EmailField(
      verbose_name='Email',
      max_length=255
  )
  names = models.CharField(max_length=200)
  password = models.CharField(max_length=200)
  phone = models.CharField(max_length=200)
  ref_nbr = models.CharField(max_length=200)
  is_active = models.BooleanField(default=True)
  is_admin = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  role = models.ForeignKey(Role,null=True,on_delete=models.CASCADE)


  USERNAME_FIELD = 'username'
 
  class Meta:
     db_table = 'Users'

# class Activity(models.Model):
#    name = models.CharField(max_length=200)
#    price = models.FloatField()
#    activity_type = models.CharField(max_length=200)
#    class Meta:
#      db_table = 'Activity'

# class Appointment(models.Model):
#    location = models.CharField(max_length=200)
#    hours_min = models.CharField(max_length=200)
#    description = models.CharField(max_length=200)
#    photographer = models.ForeignKey(Photographer,null=True,on_delete=models.CASCADE)
#    client = models.ForeignKey(Client,null=True,on_delete=models.CASCADE)
#    status = models.CharField(max_length=200)
#    payment_status = models.CharField(max_length=200)
#    class Meta:
#      db_table = 'Appointment'

# class Appointment_manager(models.Model):
#    occurance_date = models.DateTimeField(auto_now_add=True)
#    time = models.TimeField()
#    payment = models.FloatField()
#    status = models.CharField(max_length=200)
   
#    class Meta:
#      db_table = 'Appointment_manager'

