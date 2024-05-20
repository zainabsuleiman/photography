from django.db import models
import datetime
# Create your models here.




def wrapper(instance, filename):
    new_filename = str(datetime.datetime.now()).split(
        '.')[0]+'_'+str(instance.id).split('-')[0]+'__'+filename
    return 'profilePictures/'+new_filename
class Photographer(models.Model):
   firstName = models.CharField(max_length=200)
   lastName = models.CharField(max_length=200)
   phone = models.CharField(max_length=200)
   age = models.IntegerField()
   photo = models.ImageField( upload_to=wrapper, null=True, default=None)
   province = models.CharField(max_length=200)
   district = models.CharField(max_length=200)
   sector = models.CharField(max_length=200)
   streetNumber = models.CharField(max_length=200)
   years_experience = models.CharField(max_length=200)
   is_available = models.BooleanField(default=True)

   class Meta:
     db_table = 'Photographer'


class Activity(models.Model):
   name = models.CharField(max_length=200)
   price = models.FloatField()
   activity_type = models.CharField(max_length=200)
   canBeRequested=models.BooleanField(default=True)
   photographer = models.ForeignKey(Photographer,null=True,on_delete=models.CASCADE)
   class Meta:
     db_table = 'Activity'