
from django import forms
from django.contrib.auth.models import User
from main.models import products    
class ProductEditForm(forms.ModelForm):
    class Meta:
        model = products
        fields = ('product_name','prize','category','sub_category','desc','pub_date','expire_date')