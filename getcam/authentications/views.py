

# ----> actual

from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import  Profile

from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse
from .forms import loginform,UserRegistrationForm,UserEditForm,ProfileEditForm
from django.contrib import messages
from django.views import View

from django.core.mail import send_mail

from django.urls import reverse
from django.utils.encoding import force_bytes,force_text,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
import base64
from .utils import account_activation_token 

import threading

from django.core.mail import EmailMessage
from django.contrib.auth import  settings


# from .otp import send_sms,gen_otp,sms_sender



def userlogin(request):
    if request.method == 'POST':
        form = loginform(request.POST)
        if form.is_valid():
            cd  = form.cleaned_data
            user  = authenticate(request,username = cd['username'],password = cd['password'])
            if user is not None:
                if user.is_active:
                    login(request,user)
                    messages.primary(request, 'welcome ')
                    return HttpResponse("authantication successfull")
                else:
                    messages.primary(request, 'please conform your account ')
                    
                    return HttpResponse("disabled account")
            else:
                messages.primary(request, 'please conform your account ')
                return HttpResponse("invalid login")
    else:
        form = loginform()
    return render(request,'html/auth/login.html',{'form':form})


def register(request):
        if request.method == 'POST':
            user_form = UserRegistrationForm(request.POST)
            if user_form.is_valid():
                # emailcheck = User.objects.get(email = user_form.cleaned_data['email'])
                emailcheck = None
                print("checked")
                if emailcheck == None:
                    new_user = user_form.save(commit = False)
                    new_user.set_password(user_form.cleaned_data['password'])
                    new_user.is_active = False
                    new_user.save()
                    Profile.objects.create(user = new_user,id_proof = "45641")
                    email = user_form.cleaned_data['email']


                    
                    #email verfication 
                    email_verify_send(new_user,request,email)
                    messages.success(request, 'Account successfully created')
                    messe = "Account successfully created"
                    return render(request,'auth/login.html',{'new_user':new_user,'messe':messe})
                else:
                    messages.error(request,"account is already exist please try again")
                    errorr = True
                    messe = "Try Again with another email"
                    return render(request,'auth/register_done.html',{'errorr':errorr,'messe':messe})

            else:
                messages.error(request,"account is already exist please try again")
                errorr = True
                messe = "Try Again"
                return render(request,'html/auth/signup.html',{'errorr':errorr,'messe':messe})
        else:
            user_form = UserRegistrationForm()
            
     
            return render(request,'html/auth/signup.html',{'user_form' : user_form})

# email send using trading

class EmailThread(threading.Thread):
    def __init__(self, email_message):

        self.email_message = email_message
        threading.Thread.__init__(self)
                            
    def run(self):
        self.email_message.send()
def email_verify_send(new_user,request,email):
                    current_site = get_current_site(request)
                    email_body = {
                        'user':new_user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
                        'token': account_activation_token.make_token(new_user),
                    }

                    link = reverse('activate', kwargs={
                                'uidb64': email_body['uid'], 'token': email_body['token']})

                    email_subject = 'Activate your account'

                    activate_url = 'http://'+current_site.domain+link

                    email = EmailMessage(
                        email_subject,
                        'Hi '+new_user.username + ', Please the link below to activate your account \n'+activate_url,
                        'noreply@semycolon.com',
                        [email],
                    )

                    EmailThread(email).start()
                 



class verficationview(View):
    def get(self, request, uidb64, token):
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not account_activation_token.check_token(user, token):
                return redirect('login'+'?message='+'User already activated')

            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()

            messages.success(request, 'Account activated successfully')
            return redirect('login')

        except Exception as ex:
            pass

        return redirect('login')

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance = request.user,data = request.POST)
        profile_form = ProfileEditForm(instance = request.user.profile,data = request.POST,files = request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            
            user_form.save()
            profile_form.save()
            messages.success(request,"Profile updated successfully")
            return render(request,'html/auth/dashboard.html',{'user_form':user_form,'profile_form':profile_form})
        else:
            messages.error(request,'Profile updated fail')

    else:
        user_form = UserEditForm(instance = request.user)
        profile_form = ProfileEditForm(instance = request.user.profile)
    return render(request,'html/auth/edit.html',{'user_form':user_form,'profile_form':profile_form})


def profile(request):
    user = request.user
    phonenumber = user.profile.phone_verified
    number =  user.profile.phone_number
    profile_verified = user.profile.profile_verified
    print(user,phonenumber,profile_verified)
    context = {"phonenumber":phonenumber,"profile_verified":profile_verified,"number":number}
    return render(request,'html/auth/profile.html',context)





