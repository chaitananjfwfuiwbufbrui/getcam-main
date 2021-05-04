from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.
from django.shortcuts import render
from math import ceil
import json
import  datetime
from merchant.models import *
# Create your views here.
from django.shortcuts import render,HttpResponse,redirect
from main.models import *
from authentications.models import *
from  django.contrib.auth.models import User 
from django.contrib.auth import logout,authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from  django.contrib import messages
from main.pricealgo import *

from datetime import datetime ,timedelta,date
import threading
from django.views.decorators.csrf import csrf_exempt
from django.http import QueryDict
import json

from authentications.otp import send_sms,gen_otp,sms_sender
def home(request):
    
    if request.user.is_authenticated:
        Profile.objects.get_or_create(user=request.user)
        if request.method =="POST":
            # print("ASDsd")
            sos = request.POST.dict()
            sis = location(user=request.user,location=sos)
            sis.save()
            # myDict = json.loads(sos)
            # kitt = dict(myDict)

            # # sos = myDict
            # # sos= pickle.load(request.POST)
            # print(kitt,myDict,type(request.POST))
            print(str(sos.keys()))
            return JsonResponse("revived babaie",safe=False)
    dataa = products.objects.all()
    context = {'dataa' : dataa}
        
    return render(request,'phone/index.html',context)

def test(request):
    return render(request,'html/main/test.html')













# products 

def productsss(request):
       
    if request.user.is_authenticated:
        
        customer = request.user
        order ,created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitems_set.all()
        cartitems = order.get_cart_item


        latest = products.objects.filter(pub_date__range=["2020-09-17", "2020-09-18"])
        
        dataa = products.objects.all()



        user_of = Profile.objects.get(user=request.user)
        phone_verified = user_of.phone_verified 
        profile_verified = user_of.profile_verified  



        
        context = {'dataa' : dataa,'items':items,"latest":latest,'cartitems':cartitems,'phone_verified':phone_verified,"profile_verified":profile_verified}
        
        # return render(request,'html/main/gear.html',context)
    else:
         latest = products.objects.filter(pub_date__range=["2020-09-17", "2020-09-18"])
        
         dataa = products.objects.all()
            
         context = {'dataa' : dataa,"latest":latest}
        
    return render(request,'html/main/gear.html',context)

def products_fetch(request):
        return JsonResponse(les,safe=False)

def search(request):
    if 'term' in request.GET:
        qs = products.objects.filter(product_name__istartswith = request.GET.get('term'))
        titles = list()
        print(qs,titles)
        for i in qs:
                
            titles.append(i.product_name)
        print(titles)
        return JsonResponse(titles,safe=False)

    if request.method =="POST":
                name = request.POST['search']
                print(name)
                dataa = products.objects.filter(product_name = name)

                context = {'dataa' : dataa}
                return render(request,'phone/index.html',context)        
    return render(request,'test.html')




def faq(request,slug):
    print("dsfDFS")
    if request.method =="POST":

                desc = request.POST['desc']
                single = products.objects.filter(slug=slug[:-1]).first()
                print(single,slug[:-1])
                customer = request.user
                ins = faq_of_product(product_slug=single,user = customer,question = desc)
                ins.save()
                print("done for faq data")
    return redirect(f"/single/{slug[:-1]}")
def review(request,slug):
    if request.method =="POST":

                desc = request.POST['desc']
                single = products.objects.filter(slug=slug[:-1]).first()
                print(single,slug[:-1])
                customer = request.user
                ins = reviews_of_product(product_slug=single,user = customer,subject = desc,message=desc,)
                ins.save()
                print("done for the data")
    return redirect(f"/single/{slug[:-1]}")

    

def profile_and_phnumberchecker(us):
        user_of = Profile.objects.get(user=us)
        x = False 
        if user_of.phone_verified and user_of.profile_verified :


           
            x = True
            return x
        else:
            return x
def render_page(request,us,fails):
            user_of = Profile.objects.get(user=us)
            if user_of.phone_verified is  False:

                messages.info(request,f"verify your phone number  {fails}")
                return redirect("/auth/phone")
            if user_of.profile_verified is  False:

                messages.info(request,f"verify your  profile {fails}")
                return redirect('adhar')


def singleproduct(request,slug):
    
        single = products.objects.filter(slug=slug).first()
        sins = single.view_count
        sins += 1
        single.view_count = sins
        single.save()
        customer = request.user
        providers = single.provider
        product_name = single.product_name
        provider_data = Profile.objects.filter(user=providers).first()
        images_fieds = images_fiels.objects.filter(product=single)
        if request.method =="POST":
            if profile_and_phnumberchecker(request.user):
                # messages.success(request, "please verify your phone number")
                messages.error(request, "you recived a call from vendor")
                slug = request.POST['product_name']
                
                single = products.objects.filter(slug=slug).first()
                user = Profile.objects.filter(user=customer).first()
                messages_otp = f'''
                you  have a order from {user.user} \n phone:  {user.phone_number} \n order on : {product_name}   \n                 
                '''
                sms_sender(provider_data.phone_number,messages_otp)
                sos = requested_delivary(product=single,customer=request.user)
                sos.save()
            else:
                messages.error(request, "please verify your number")
                
                return render_page(request, request.user, "ass")
                print("ASDSDSDASDS")

        context = {'single' : single,"providers":provider_data,"images":images_fieds}
        return render(request,'phone/singleproduct.html',context)

  

def provider(request):
    if request.method =="POST":
            selected_provider = request.POST['cars']
            print(selected_provider)
            return redirect(f"/single/{selected_provider}")
def about(request):

    return render(request,'html/main/about.html')



def cart(request):
    customer = request.user
    order ,created = Order.objects.get_or_create(customer=customer,complete=False)
    items = order.orderitems_set.all()
    cartitems = order.get_cart_item



    
    items = order.orderitems_set.all()
    context = {'items':items,'order':order,'cartitems':cartitems}


    return render(request,'html/main/cart.html',context)


def updatecart(request):
    data = json.loads(request.body)
    productid = data['productsid']
    action = data['action']
    
    customer = request.user
    product = products.objects.get(id=productid)
    order ,created = Order.objects.get_or_create(customer=customer,complete=False)
    orderitems ,created = Orderitems.objects.get_or_create(order=order,product=product)
    cartitems = order.get_cart_item
    if action == 'add':
        
        orderitems.quantity = (orderitems.quantity + 1)

    elif action == "remove":
            orderitems.quantity = (orderitems.quantity-1)
    elif action == 'delete':
        orderitems.quantity = 0


    orderitems.save()
    if orderitems.quantity <= 0 :
            orderitems.delete()
    

    return JsonResponse("your cart is added",safe=False)



def processorder(request):
    print('data:',request.body)
    customer = request.user
    transection_id = datetime.now().timestamp
    order ,created = Order.objects.get_or_create(customer=customer,complete=False)

    data = json.loads(request.body)
    total = float(data['form']['total'])
    order.transaction_id = transection_id
    print(transection_id)
    if total == order.get_cart_total:
        order.complete = True
    order.complete = True
    order.save()

    #merchant prblm
    s = Orderitems.objects.filter(order = order)
    sosso = ['JANUARY', 'FEBRUARY', 'MARCH', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'DECEMBER']
    current_date = date.today() 
    sa = current_date.month
    present_month = sosso[sa-1]
    for i in s:
        merchant  = i.product.provider
        print(merchant)
        pro = mechant.objects.get(mechant=merchant) 
        # print(pro)
        swq = monthly_revunue.objects.get(merchant=pro,month=present_month)
        swq.no_of_orders += 1
        swq.revunue += i.product.prize
        swq.save()


    if order.complete == True:
        ShippingOrder.objects.create(
            customer = customer,
            order = order,
            
            address =data['shipping']['address'],
            city = data['shipping']['country'],

            zipcode = data['shipping']['zip'],
            
            state =  data['shipping']['state'],
        )
         
    return JsonResponse("payment has been done....",safe=False)

def checkout(request):
    customer = request.user
    order ,created = Order.objects.get_or_create(customer=customer,complete=False)
    items = order.orderitems_set.all()
    cartitems = order.get_cart_item
    context = {'items':items,'order':order,'cartitems':cartitems}
    
    if profile_and_phnumberchecker(request,customer,"welcome to check out enter the details to process order") is False:
        
    
        return render_page(request,customer,"to get in to checkout page")
    print(profile_and_phnumberchecker(request,customer,"welcome to check out enter the details to process order") )
    return render(request,'html/main/checkout.html',context)

def testcheck(request):
    
    orders = Order.objects.filter(customer=request.user,complete=True).first()
    # s = Orderitems.objects.filter(order = order)
    s = Orderitems.objects.filter(order = orders)
    
    for i in s:
        merchant  = i.product.provider
        print(merchant)
        pro = mechant.objects.get(mechant=merchant) 
        # print(pro)
        swq = monthly_revunue.objects.get(merchant=pro,month="April")
        swq.no_of_orders += 1
        swq.save()


    
    return render(request,'html/main/test2.html')


def email_subscribe(request):
    
    if request.method =="POST":
            email = request.POST['subscribe_email']
            print(email)
            mail = subscribedmaile(email=email)
            mail.save()
            messages.success(request,"credentials recived")
            return redirect('home')     