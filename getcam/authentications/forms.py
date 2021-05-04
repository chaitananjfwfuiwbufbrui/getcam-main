from django import forms
from django.contrib.auth.models import User
from .models import Profile
class loginform(forms.Form):
    username = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter username',}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}))


class  UserRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(label = 'username', widget=forms.Textarea(attrs={'placeholder': 'Enter your name',}),required=True)
    username = forms.CharField(label = 'username', widget=forms.Textarea(attrs={'placeholder': 'Enter username',}),required=True)
    email = forms.CharField(label = 'email', widget=forms.Textarea(attrs={'placeholder': 'Enter Email'}),required=True)
    phonenumber = forms.CharField(label = 'email', widget=forms.Textarea(attrs={'placeholder': 'Enter phonenumber'}),required=True)
    password = forms.CharField(label = 'Password', widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}),required=True)
    password2 = forms.CharField(label = 'Repeat Password',widget=forms.PasswordInput(attrs={'placeholder': 'Re-Enter password'}),required=True)
    class Meta:
        model = User
        fields = ('username', 'email','first_name')
        def clean_password2(self):
            cd = self.cleaned_data
            if cd['password'] != cd['password2']:
                raise  forms.ValidationError("password don't match")
            return cd['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name','last_name','email')
    
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone_number','otp')

        
# class PhoneEditForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ('phone_number')
    