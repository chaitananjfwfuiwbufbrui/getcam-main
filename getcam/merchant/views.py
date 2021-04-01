from django.shortcuts import render,redirect,HttpResponse
from main.models import *
from authentications.models import *
from .forms import *
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
def edit_product(request,slug):

    if request.method == 'POST':
        s = products.objects.filter(slug = slug).first()
        
        # profile_form = ProfileEditForm(instance = request.user.profile,data = request.POST,files = request.FILES)
        product_form = ProductEditForm(instance = s,data = request.POST)
        if product_form.is_valid():
            
            
            product_form.save()
            # messages.success(request,"Profile updated successfully")
            return redirect('merchant')
            
        else:
            # messages.error(request,'Profile updated fail')
            HttpResponse("404 erroe")

    else:

        s = products.objects.filter(slug = slug).first()
        product_form = ProductEditForm(instance = s)
        context = {"product_form":product_form,"products":s}
    return render(request, 'mc/edit_form.html',context)
    