from django.shortcuts import render, redirect, HttpResponse
from main.models import *
from authentications.models import *
from .forms import *
# Create your views here.
from .models import *

def home(request):
    user = request.user
    list_of = products.objects.filter(provider=user)
    # print(list_of)
    context = {"products": list_of}
    return render(request, 'mc/home.html', context)

def delete_product(request,slug):
    delll = products.objects.filter(slug = slug).first()
    delll.delete()
    return redirect('merchant')
def product_view(request, slug):
    user = request.user
    list_of = products.objects.filter(provider=user, slug=slug).first()
    images = images_fiels.objects.filter(product=list_of)
    print(list_of)
    context = {"products": list_of, "images": images}
    return render(request, 'mc/pageadd.html', context)


def edit_product(request, slug):

    if request.method == 'POST':
        s = products.objects.filter(slug=slug).first()

        # profile_form = ProfileEditForm(instance = request.user.profile,data = request.POST,files = request.FILES)
        product_form = ProductEditForm(instance=s, data=request.POST)
        if product_form.is_valid():

            product_form.save()
            # messages.success(request,"Profile updated successfully")
            return redirect('merchant')

        else:
            # messages.error(request,'Profile updated fail')
            HttpResponse("404 erroe")

    else:

        s = products.objects.filter(slug=slug).first()
        product_form = ProductEditForm(instance=s)
        imageya = images_fiels.objects.filter(product = s)
        context = {"product_form": product_form, "products": s,"imageya":imageya}
    return render(request, 'mc/edit_form.html', context)


def test(request):
    return render(request, 'mc/test.html')


def product_add(request):
    if request.method == 'POST' and 'product_images' in request.FILES:

        product_image = request.FILES['product_images']
        # product_image = img['product_images']

        product_name = request.POST['product_name']
        Prize = request.POST['Prize']
        catagiory = request.POST['catagiory']
        subcatagiory = request.POST['subcatagiory']
        description = request.POST['description']
        pub_date = request.POST['pub_date']
        expire_date = request.POST['expire_date']
        provider = request.user
        is_availble = True
        print(product_name)
        ins = products(provider=provider,product_image=product_image,product_name=product_name,prize=Prize,category=catagiory,sub_category=subcatagiory,desc=description,pub_date=pub_date,expire_date=expire_date,is_availble=is_availble)
        ins.save()
        # print("done for the data")
        return redirect("merchant")
    return render(request, 'mc/product_add.html')
def addimg(request,slug):
    if request.method == 'POST' and 'product_images1' in request.FILES:
        product_image = request.FILES['product_images1']
        pro = products.objects.filter(slug = slug).first()

        ins = images_fiels(product = pro,product_image = product_image)
        ins.save()
        print("yes")

    return redirect('edit_product',slug)
def dash(request):
    from datetime import date
# creating the date object of today's date
    s = ['JANUARY', 'FEBRUARY', 'MARCH', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'DECEMBER']
    current_date = date.today() 
    sa = current_date.month
    
    present_month = s[sa-1]
    pro = mechant.objects.get(mechant=request.user ) 
    # print(pro.completed_orders)
    for i in range(12):
        
        mon = monthly_revunue.objects.get_or_create(merchant=pro,month = s[i],year=2021)
    mon = monthly_revunue.objects.filter(merchant=pro)
    # print(mon)
    datalabeles = []
    datalabeless = []
    monthly_revun = monthly_revunue.objects.filter(merchant=pro,month=present_month,year=2021).first()
    # print(monthly_revun.revunue)
    month_revnues = monthly_revun.revunue
    year_revnue = 0
    orders = 0
    for i in mon:
        # print(i.month,":",i.revunue)
        datalabeles.append(i.revunue) 
        year_revnue += i.revunue
        datalabeless.append(i.no_of_orders)
        orders += i.no_of_orders
    pro.total_order = orders
    pro.revunue = year_revnue
    pro.save()
    shedule_orders = orders - pro.completed_orders
    print(year_revnue)   
    context = {'datalabeles':datalabeles,"datalabeless":datalabeless,"month_revnues":month_revnues,"year_revnue":year_revnue,"orders":orders,"shedule_orders":shedule_orders}
    return render(request,'mc/dashboard.html',context)