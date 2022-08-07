# from dataclasses import field
# import imp
from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model=Order
        fields=['first_name','last_name','email','address_line_1','address_line_2','phone','country','city','state']