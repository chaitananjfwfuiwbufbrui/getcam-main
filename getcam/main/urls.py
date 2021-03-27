from django.contrib import admin
from django.urls import path,include
from main import views
from django.conf import settings
from django.contrib.auth import views as auth_views
urlpatterns = [
   
     path('', views.home, name='home'),
     path('test/', views.testcheck, name='test'),
     path('search/', views.search, name='search'),
     path('cart/', views.cart, name='cart'),
     path('updatecart/', views.updatecart, name='updatecart'),



     path('checkout/', views.checkout, name='checkout'),
     path('processorder/', views.processorder, name='processorder'),
     path('products/', views.productsss, name='products'),
     path('single/<str:slug>',views.singleproduct,name ='singleproduct'),
     path('review/<str:slug>',views.review,name ='review'),
     path('faq/<str:slug>',views.faq,name ='faq'),
     path('provider/',views.provider,name ='provider'),
     path('about/',views.about,name ='about'),
     path('email_subscribe/',views.email_subscribe,name ='email_subscribe'),

    
]