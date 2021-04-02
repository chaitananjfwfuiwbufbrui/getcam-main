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
    pro = mechant.objects.get(mechant=request.user ) 
    print(pro.completed_orders)
    s = ['JANUARY', 'FEBRUARY', 'MARCH', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'DECEMBER']
    for i in range(12):
        print(i,s[i])
        mon = monthly_revunue.objects.get_or_create(merchant=pro,month = s[i],revunue=0)
    mon = monthly_revunue.objects.filter(merchant=pro)
    print(mon)
    datalabeles = []
    for i in mon:
        print(i.month,":",i.revunue)
        datalabeles.append(i.revunue) 
    print(datalabeles)   
    datalabeless = [0, 10, 5, 25, 20, 300, 45]
    context = {'datalabeles':datalabeles,"datalabeless":datalabeless}
    return render(request,'mc/dashboard.html',context)