from django.db import models
from django.contrib.auth.models import User
from authentications.models import *
# Create your models here.

from django.db import models
from django.db.models.signals import pre_save
from getcam.utils import unique_slug_generator
import requests

class subscribedmaile(models.Model):
    email =  models.EmailField(max_length=254)
    subscribed_date = models.DateTimeField(auto_now_add=True)
# Create your models here.
class products(models.Model):
    view_count = models.IntegerField(default=0)
    provider = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True)
    product_id = models.AutoField
    product_name = models.CharField( max_length=50)
    prize = models.IntegerField(default=0)
    category = models.CharField(max_length=50,default="")
    sub_category = models.CharField(max_length=50,default="")
    product_image =models.ImageField(upload_to="shop/images",default="")
    desc = models.CharField(max_length=300)

    pub_date = models.DateField()
    expire_date = models.DateField()

    slug = models.SlugField(blank=True,null=True)
    is_availble = models.BooleanField(default=True)



    def __str__(self):
        return self.product_name +"         catagiory:   " +self.category + "subcatagiry :   "+ self.sub_category
class location(models.Model):
    user  = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True)
    location =models.CharField(max_length=300)

class images_fiels(models.Model):
    product = models.ForeignKey(products,on_delete=models.SET_NULL,blank=True,null=True)
    product_image =models.ImageField(upload_to="shop/images",default="")






def slug_generator(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
pre_save.connect(slug_generator,sender=products)

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name
class contact(models.Model):
            message = models.AutoField(primary_key=True)
            name = models.CharField(max_length=30,default="")
            email = models.CharField(max_length=30,default="")
            phn = models.CharField(max_length=20,default="")
            desc = models.CharField(max_length=200,default="")
            def __str__(self):
                return self.name




class Order(models.Model):
    customer = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True)
    data_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False,null=True,blank=True)
    transaction_id = models.CharField(max_length=100,null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitemss = self.orderitems_set.all()
        
        total = sum([item.get_total for item in orderitemss])
        return  total

    @property
    def get_cart_item(self):
        orderitemss = self.orderitems_set.all()
        total = sum([item.quantity for item in orderitemss])
        return  total

class requested_delivary(models.Model):
    product = models.ForeignKey(products,on_delete=models.SET_NULL,blank=True,null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True)    

class   Orderitems(models.Model):
    product = models.ForeignKey(products,on_delete=models.SET_NULL,blank=True,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    quantity = models.IntegerField(default=0,null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    @property
    def get_total(self):
        total = self.product.prize * self.quantity
        return total


class ShippingOrder(models.Model):
    customer = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    address= models.CharField(max_length=100,null=True)
    city = models.CharField(max_length=100,null=True)
    zipcode = models.IntegerField(null=True)
    state = models.CharField(max_length=100,null=True)
    date_added = models.DateTimeField(auto_now_add=True)


class essential_details(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True)
    no_of_orders = models.IntegerField(default=0)
    completed_orders = models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    product = models.ForeignKey(Orderitems,on_delete=models.SET_NULL,blank=True,null=True)
    address = models.ForeignKey(ShippingOrder,on_delete=models.SET_NULL,blank=True,null=True)

class prize_chart(models.Model):
    product_slug = models.ForeignKey(products,on_delete=models.SET_NULL,blank=True,null=True)
    orginal_prize = models.IntegerField(default=0)
    day =  models.IntegerField(default=0)
    disccount = models.IntegerField(default=0)
    prize = models.IntegerField(default=0)

class reviews_of_product(models.Model):
    product_slug = models.ForeignKey(products,on_delete=models.SET_NULL,blank=True,null=True)
    user = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True)
    subject = models.CharField(max_length=30,default="")
    message = models.CharField(max_length=150,default="")
class faq_of_product(models.Model):
    product_slug = models.ForeignKey(products,on_delete=models.SET_NULL,blank=True,null=True)
    user = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True)
    
    question = models.CharField(max_length=150,default="")
    answer = models.CharField(max_length=150,default="")
    complted = models.BooleanField(default= False)