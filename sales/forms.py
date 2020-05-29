from django import forms
from .models import Stock, Invoice, Customer
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class Form1(forms.ModelForm):
    name = forms.CharField(max_length=100, label='name')
    phone = forms.CharField(max_length=100, label='phone')
    place = forms.CharField(max_length=100, label='place')
    date_created = forms.DateTimeField(label='date')

    class Meta:
        model = Customer
        fields = '__all__'


class Form2(forms.ModelForm):
    product_name = forms.CharField(max_length=100, label='product name')
    company_name = forms.CharField(max_length=100, label='company name')
    quantity = forms.FloatField(label='quantity')
    price = forms.FloatField(label='price')
    date_created = forms.DateTimeField(label='date')

    class Meta:
        model = Stock
        fields = '__all__'


class Form3(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = '__all__'
        exclude = ['total']


class Form4(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = '__all__'
        exclude = ['place', 'date_created', 'total']


class CreateUserform(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
