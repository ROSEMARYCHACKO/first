from distutils.command.upload import upload
from unicodedata import name
from xml.parsers.expat import model
from django.db import models

# Create your models here.

class Service_provider(models.Model):
    email = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    name = models.CharField(max_length=30)

class Products(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=250)
    rate = models.CharField(max_length=50)
    count = models.IntegerField()
    image = models.ImageField(upload_to='images/')

class Users(models.Model):
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    address = models.CharField(max_length=30)
    phone = models.CharField(max_length=30)
class Order(models.Model):
    name = models.CharField(max_length=30)
    user_id = models.CharField(max_length=50)
    rate = models.CharField(max_length=50)
    count = models.IntegerField()
    image = models.ImageField(upload_to='images/')
    service_provider = models.CharField(max_length=250)
    status = models.CharField(max_length=250)
    date = models.CharField(max_length=250)


#chat model
class Chat(models.Model):
    user_type = models.CharField(max_length=50)
    user_name = models.CharField(max_length=50)
    user_id = models.IntegerField()
    comment = models.CharField(max_length=250)
    status = models.IntegerField()
    date = models.CharField(max_length=250)

#soiol test model
class Soil_test(models.Model):
    user_name = models.CharField(max_length=50)
    user_id = models.IntegerField()
    comment = models.CharField(max_length=250)
    service_provider = models.CharField(max_length = 50)
    service_provider_id = models.IntegerField()
    results = models.CharField(max_length=250)
    status = models.CharField(max_length=20)
    date = models.CharField(max_length=250)
    flag = models.IntegerField()