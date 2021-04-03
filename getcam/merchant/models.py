# from django.db import modefrom django.db import models
from django.contrib.auth.models import User
from authentications.models import *
# Create your models here.

from django.db import models
from django.db.models.signals import pre_save
from getcam.utils import unique_slug_generator
from main.models import *
import requests



class mechant(models.Model):

    mechant = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True)
    product = models.OneToOneField(products, null=True, blank=True, on_delete=models.CASCADE)

    revunue =  models.IntegerField(default=0)
    
    today =  models.IntegerField(default=0)
    total_order = models.IntegerField(default=0)
    completed_orders = models.IntegerField(default=0)

class monthly_revunue(models.Model):
    merchant =  models.ForeignKey(mechant, null=True, blank=True, on_delete=models.CASCADE)

    MONTH_CHOICES = (
        ("JANUARY", "January"),
        ("FEBRUARY", "February"),
        ("MARCH", "March"),
        ("April","April"),
        ("May","May"),
        ("June","June"),
        ("July","July"),
        ("August","August"),
        ("September","September"),
        ("October","October"),
        ("November","November"),
        ("DECEMBER", "December"),
    )
    month = models.CharField(max_length=9,choices=MONTH_CHOICES)
    revunue = models.IntegerField(default=0)
    year = models.IntegerField(default=0)
    no_of_orders = models.IntegerField(default=0)
    def __str__(self):
                return f"year:{self.year} , month : {self.month},merchant : {self.merchant}" 