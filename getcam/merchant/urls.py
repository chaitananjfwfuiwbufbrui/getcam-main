from django.contrib import admin
from django.urls import path,include
from merchant import views
from django.conf import settings
from django.contrib.auth import views as auth_views
urlpatterns = [
   
     path('', views.home, name='merchant'),
     path('test/', views.test, name='test'),
     path('dash/', views.dash, name='dash'),
     path('product_add/', views.product_add, name='product_add'),
     path('product_view/<str:slug>', views.product_view, name='product_add'),
     path('edit_product/<str:slug>', views.edit_product, name='edit_product'),
     path('delete_product/<str:slug>', views.delete_product, name='delete_product'),
     path('addimg/<str:slug>', views.addimg, name='addimg'),
]