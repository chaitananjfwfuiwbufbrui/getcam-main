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
from  django.contrib.auth.models import User 
from django.contrib.auth import logout,authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from  django.contrib import messages
from main.pricealgo import *

from datetime import datetime ,timedelta,date
import threading


def home(request):
    popup = True
      
    if request.user.is_authenticated:
        # creating profile for people who logged in by facebook
        Profile.objects.get_or_create(user = request.user)

        # merchant account stuff

        group = None
        merchant = False
       
        user_name = request.user
        
        if request.user.groups.exists():
            # extracting the account detailes for view
            group = request.user.groups.all()[0].name
            if group == 'merchant':
                
                merchant = True
                
        # for recommandation stuff  
        now = datetime.now()
        last = date.today() - timedelta(days=30)
        timestamp = datetime.date(now)

            
            
        order ,created = Order.objects.get_or_create(customer=user_name,complete=False)
        items = order.orderitems_set.all()
        cartitems = order.get_cart_item

        latest = products.objects.filter(pub_date__range=[last, timestamp])
        # <-------products extraction ------->
        # <-------here we need   a recommendation system ------->

        dataa = products.objects.all()           
                    
        context = {'dataa' : dataa,"latest":latest,'cartitems':cartitems,'merchant':merchant,"popup":popup}
    else:

        if request.method =="POST":
            close = request.POST['close']
            popup = False
            print(close)
            
            
        latest = products.objects.filter(pub_date__range=["2020-09-17", "2021-12-25"])
            
        dataa = products.objects.all()
        context = {'dataa' : dataa,"latest":latest,"popup":popup}
        
    return render(request,'html/main/index.html',context)

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



def search(request):
    if 'term' in request.GET:
        qs = products.objects.filter(product_name__istartswith = request.GET.get('term'))
        titles = list()
        print(qs,titles)
        for i in qs:
                
            titles.append(i.product_name)

        return JsonResponse(titles,safe=False)

    if request.method =="POST":
                name = request.POST['search']
                print(name)
                dataa = products.objects.filter(product_name = name)

                context = {'dataa' : dataa}
                return render(request,'html/main/gear.html',context)        
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


def singleproduct(request,slug):
    if request.user.is_authenticated:
        single = products.objects.filter(slug=slug).first()
        customer = request.user
        order ,created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitems_set.all()
        cartitems = order.get_cart_item
        days = 1
        if request.method =="POST":
            expire = request.POST['exper']
            arrival = request.POST['arrival']
            days = (int(expire[3:5]) - int(arrival[3:5])) + 1
            
        #algo for pricing 
        single = products.objects.filter(slug=slug).first()
        prize = model1(single.prize,days)
        single_prize = single.prize * days
        imageya = images_fiels.objects.filter(product = single)
        def date_convetor(date):

            s = str(date)
            a = s.split("-")
            xz =  [int(s) for s in a] 
            return xz[0],xz[1],xz[2]
        # print(date_convetor(single.pub_date),type(date_convetor(single.pub_date)))
        
        from datetime import date, timedelta
        isi = date_convetor(single.pub_date)
        esi = date_convetor(single.expire_date)
        sdate = date(isi[0],isi[1],isi[2])  # start date
        edate = date(esi[0],esi[1],esi[2])   # end date

        delta = edate - sdate   
        
        
        # as timedelta
        availbe_dates_list = []

        # #prize chart
        s_no = [1,2,3,4,5,6,7]
        

        for i in s_no:
            filled = model1(single.prize,i)
            org = single.prize*i
            
            prize_chart.objects.get_or_create(product_slug = single,day = i,orginal_prize =org ,disccount=filled[0] , prize =filled[2] )

        # <______done _________>

        checkone  = prize_chart.objects.filter(product_slug = single)
       
        for i in range(delta.days + 1):
            day = sdate + timedelta(days=i)
            sos = str(day)
            k = sos[8:] + sos[4:8] + sos[:4]
            
            availbe_dates_list.append(k)
      


        all_obj = products.objects.filter(product_name=single.product_name)

        
        #algo for pricing ^^^^^^
        




        #cart check 
        orde = Order.objects.filter(customer = customer).first()
        prod = Orderitems.objects.filter(order = orde)
        already_ther = False
        for i in prod:
            if i.product.slug == slug:

                already_ther = True
            

        reviews =reviews_of_product.objects.filter(product_slug=single)
        faq =faq_of_product.objects.filter(product_slug=single)
        print(faq)
        reviews_count =True
        if len(reviews) == 0:
            
            reviews_count = False


        prod = products.objects.filter(sub_category=single.sub_category)
        subheading = products.objects.filter(category=single.category)
        
        removelis = [single.product_name]
        new_list = []
        newcat = []
        #filtering single product from our sub catagiory set
        for i in prod:
            if not i.product_name in removelis:
                new_list.append(i)
        #filtering single product from our sub catagiory set            
        for s in subheading:
            if not s.product_name in removelis:
                newcat.append(s)
        #filtering sub catagiory  product from our catagiory set
        for q in new_list:
            if q in newcat:
                newcat.remove(q)
        
        context = {'single' : single,"faq":faq,"reviews_count":reviews_count,"review_obj":reviews,"prod":new_list,"catagory":newcat,'cartitems':cartitems,"imageya":imageya,"all_obj":all_obj,"already_ther":already_ther,'prize':ceil(prize[0]),'discount': prize[2],'availbe_dates_list':availbe_dates_list,'days':days,'checkone':checkone,'single_prize':single_prize}
        return render(request,'html/main/singleproduct.html',context)

    else:
        single = products.objects.filter(slug=slug).first()
        imageya = images_fiels.objects.filter(product = single)
        days = 1
        prize = model1(single.prize,days)
        # print(prize[2],type(prize))
        
        prod = products.objects.filter(sub_category=single.sub_category)
        subheading = products.objects.filter(category=single.category)
        
        removelis = [single.product_name]
        new_list = []
        newcat = []
        #filtering single product from our sub catagiory set
        for i in prod:
            if not i.product_name in removelis:
                new_list.append(i)
        #filtering single product from our sub catagiory set            
        for s in subheading:
            if not s.product_name in removelis:
                newcat.append(s)
        #filtering sub catagiory  product from our catagiory set
        for q in new_list:
            if q in newcat:
                newcat.remove(q)
        
        context = {'single' : single,"prod":new_list,"catagory":newcat,"imageya":imageya,'prize':ceil(prize[0]),'discount': prize[2]}
        return render(request,'html/main/singleproduct.html',context)

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
    
    # data = json.loads(request.body)
    # count=request.body['count']

    print("hello")

    # print("count status ",count)
    return render(request,'html/main/test2.html')

    

def profile_and_phnumberchecker(request,us,succes):
        user_of = Profile.objects.get(user=us)
        x = False 
        if user_of.phone_verified and user_of.profile_verified :


            messages.success(request,f"{succes}!!")
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


def email_subscribe(request):
    
    if request.method =="POST":
            email = request.POST['subscribe_email']
            print(email)
            mail = subscribedmaile(email=email)
            mail.save()
            messages.success(request,"credentials recived")
            return redirect('home')     