from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.
from django.shortcuts import render
from math import ceil
import json
import  datetime
# Create your views here.
from django.shortcuts import render,HttpResponse,redirect
from main.models import *
from authentications.models import *
# from  django.contrib.auth.models import User 
# from django.contrib.auth import logout,authenticate
# from django.contrib.auth.forms import AuthenticationForm
# from django.contrib.auth import login as auth_login
# from  django.contrib import messages


# from datetime import datetime ,timedelta,date
# import threading


def home(request):
    if request.user.is_authenticated:
        Profile.objects.get_or_create(user = request.user)
    return render(request,'html/main/index.html')