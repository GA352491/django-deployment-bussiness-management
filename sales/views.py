from django.shortcuts import render, redirect
from .models import Invoice, Stock, Tag, Customer
from .forms import Form1, Form2, Form3, Form4, CreateUserform
import pandas as pd
from django.forms import inlineformset_factory
from .filters import InvoiceFilter
from django.db.models import Value, FloatField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Create your views here.
@login_required(login_url='login')
def home(request):
    orders = Invoice.objects.all()
    customers = Customer.objects.all()
    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'orders': orders, 'customers': customers, 'total_customers': total_customers,
               'total_orders': total_orders, 'delivered': delivered, 'pending': pending}

    return render(request, 'home.html', context)

@login_required(login_url='login')
def stock(request):
    products = Stock.objects.all()
    df = pd.DataFrame(list(Invoice.objects.all()))
    # df2 = df.groupby(['customer_name_id']).agg('sum')

    #################################################

    df = pd.DataFrame(list(Invoice.objects.all().values()))
    df1 = pd.DataFrame(list(Stock.objects.all().values()))

    df3 = df.groupby(['product_name_id']).sum()

    df1.columns = ['product_name_id', 'product name', 'company name', 'quantity', 'price', 'date created',
                   'stock available']
    # print(df1.keys())
    df4 = pd.merge(df1, df3, on='product_name_id',how='left')
    # print(df4)
    df4['stock available'] = df4['quantity'] - df4['no_of_products']
    df4.rename(columns={'price_x': 'price'}, inplace=True)
    # print(df4)
    a = df4[['product name', 'company name', 'quantity', 'price', 'date created', 'stock available']]

    # s = Stock.objects.update_or_create(stock_available=num, defaults={})

    #print(df4)
    con = [products, a]
    com_count = df4['company name'].nunique()
    context = {'products': products, 'a': a, 'df4': df4, 'con': con, 'com_count': com_count}

    return render(request, 'stock.html', context)

@login_required(login_url='login')
def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    ord = Invoice.objects.filter(customer_name_id=pk).count()
    # orders = Customer.objects.filter(id=pk)
    orders1 = Invoice.objects.filter(customer_name_id=pk)
    myFilter = InvoiceFilter(request.GET, queryset=orders1)
    orders1 = myFilter.qs

    context = {'customer': customer, 'ord': ord, 'orders1': orders1, 'myFilter': myFilter}
    return render(request, 'customer.html', context)

@login_required(login_url='login')
def create_invoice(request):
    a = Invoice.objects.all()
    form = Form3()
    if request.method == 'POST':
        form = Form3(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form, 'a': a}
    return render(request, 'order.html', context)

@login_required(login_url='login')
def update_invoice(request, pk):
    order = Invoice.objects.get(id=pk)
    form = Form3(instance=order)

    if request.method == 'POST':
        form = Form3(request.POST, instance=order)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'order.html', context)

@login_required(login_url='login')
def delete_invoice(request, pk):
    order = Invoice.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('home')

    context = {'item': order}
    return render(request, 'delete.html', context)

@login_required(login_url='login')
def customer_list(request):
    customers = Customer.objects.all()
    context = {'customers': customers}

    return render(request, 'customer list.html', context)

@login_required(login_url='login')
def dataset(request):
    df = pd.DataFrame(list(Invoice.objects.all().values()))
    df1 = pd.DataFrame(list(Stock.objects.all().values()))

    df3 = df.groupby(['product_name_id']).sum()

    df1.columns = ['product_name_id', 'product_name', 'company_name', 'quantity', 'price', 'date_created']
    # print(df1)
    df4 = pd.merge(df1, df3, on='product_name_id')
    # print(df4)
    df4['remaining'] = df4['quantity'] - df4['no_of_products']
    # print(df4)
    a = df4['remaining']

    # print(a)

    context = {'df4': df4, 'a': a}

    return render(request, 'customer list.html', context)

@login_required(login_url='login')
def place_order(request, pk):
    Form4Set = inlineformset_factory(Customer, Invoice, fields=('product_name', 'no_of_products', 'price', 'status'),
                                     extra=2)
    customer = Customer.objects.get(id=pk)
    form = Form4Set(queryset=Invoice.objects.none(), instance=customer)
    # form = Form4(initial={'customer_name': customer})
    if request.method == 'POST':
        form = Form4(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'place order.html', context)

@login_required(login_url='login')
def create_cust(request):
    form = Form1()
    if request.method == 'POST':
        form = Form1(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customerlist')

    context = {'form': form}
    return render(request, 'create_customer.html', context)

@login_required(login_url='login')
def stock_create(request):
    form = Form2()
    if request.method == 'POST':
        form = Form2(request.POST)
        if form.is_valid():
            form.save()
            return redirect('stock')
    context = {'form': form}
    return render(request, 'stock create.html', context)


def registerpage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:


        form = CreateUserform()

        if request.method == 'POST':
            form = CreateUserform(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)
                return redirect('login')

        context = {'form': form}
        return render(request, 'register.html', context)


def loginpage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, "username or password is incorrect")
                return render(request, 'login.html', )

        context = {}
        return render(request, 'login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def delete_customer(request, pk):
    order = Customer.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('home')

    context = {'item': order}
    return render(request, 'deletecustomer.html', context)

@login_required(login_url='login')
def update_customer(request, pk):
    order = Customer.objects.get(id=pk)
    form = Form1(instance=order)

    if request.method == 'POST':
        form = Form1(request.POST, instance=order)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'create_customer.html', context)

