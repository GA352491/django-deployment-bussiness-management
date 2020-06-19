from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from datetime import datetime, date
import pandas as pd


# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=100, null=True)
    place = models.CharField(max_length=100, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name


class Stock(models.Model):
    product_name = models.CharField(max_length=100, null=True)
    company_name = models.CharField(max_length=100, null=True)
    quantity = models.FloatField(null=True)
    price = models.FloatField(null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    tags = models.ManyToManyField(Tag)
    stock_available = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.product_name


class Invoice(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Out of delivery', 'Out of delivery'),
        ('Delivered', 'Delivered'),
    )
    customer_name = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    product_name = models.ForeignKey(Stock, null=True, on_delete=models.SET_NULL)
    place = models.CharField(max_length=100, null=True)
    no_of_products = models.FloatField(null=True)
    price = models.FloatField(null=True)
    total = models.FloatField(null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=100, null=True, choices=STATUS)
    invoice_no = models.CharField(null=True, max_length=100)

    def __str__(self):
        return self.status

    @property
    def get_total(self):
        total = self.price * self.no_of_products
        a = Invoice.objects.get(id=self.id)
        a.total = total
        a.save()
        return total

    @property
    def increment_number(self):
        df = pd.DataFrame(list(Invoice.objects.all().values()))
        last_invoice = df['invoice_no'].iloc[-1]
        num = str('SRI00') + str(self.id)
        a = Invoice.objects.get(id=self.id)
        a.invoice_no = num
        a.save()
        return num
