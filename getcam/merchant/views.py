from django.shortcuts import render
from main.models import *
from authentications.models import *
# Create your views here.
def home(request):
    user = request.user
    list_of = products.objects.filter(provider = user)
    # print(list_of)
    context = {"products":list_of}
    return render(request, 'mc/home.html',context)
def product_add(request,slug):
    user = request.user
    list_of = products.objects.filter(provider = user,slug = slug).first()
    images = images_fiels.objects.filter(product = list_of)
    print(list_of)
    context = {"products":list_of,"images":images}
    return render(request, 'mc/pageadd.html',context)