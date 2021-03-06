


from django.contrib.auth import views as auth_views
from django.urls import path,include
from . import views



from .views import verficationview

urlpatterns = [
    
    
    path('register/', views.register,name='register'),
    path('edit/', views.edit,name='edit'),
    path('profile/', views.profile,name='profile'),
    
     
    path('login/', views.userlogin,name='login'),
    path('logout/', auth_views.LogoutView.as_view(),name='logout'),
    # password change view
    path('password_change/', auth_views.PasswordChangeView.as_view(),name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(),name='password_done'),

    # password reset
    path('password_reset/', auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),name='password_reset_conformview'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),



    path('activate/<uidb64>/<token>/', verficationview.as_view(),name='activate'),

# verifications are here
    path('phone/', views.phone_number,name='phone'),
    path('verify_number/', views.verify_number,name='verify-number'),

# 
    path('adhar/', views.adhar,name='adhar'),
]


