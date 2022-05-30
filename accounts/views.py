from ast import unaryop
from cmath import log
from email.headerregistry import Group
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from accounts.decorators import unauthenticated_user
from .models import*
from .forms import OrderForm, CreateUserForm, CustomerForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import *

from django.http import JsonResponse


# Create your views here.
@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username =request.POST.get('username')
        password =request.POST.get('password')
            
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect')
    context = {}
    return render(request, 'accounts/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')

@unauthenticated_user
def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')      
            messages.success(request, 'Account created succesfully. Welcome '+ username)
            return redirect('login')
    context = {'form':form}
    return render(request, 'accounts/register.html', context)


@login_required(login_url='login')
@admin_only
def home(request):
    customers = Customers.objects.all()
    orders = Order.objects.all()
    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status ='Delivered').count()
    pending = orders.filter(status ='Pending').count()
    context = {'orders':orders, 'customers':customers, 'total_orders':total_orders, 'delivered':delivered, 'pending':pending}
    return render(request, 'accounts/dashboard.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products':products})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk):
    customers = Customers.objects.get(id=pk)
    
    orders = customers.order_set.all()
    total_orders = orders.count()
      
    
    context = {'customers':customers, 'orders':orders, 'total_orders':total_orders}
    return render(request, 'accounts/customer.html', context)

@login_required(login_url='login')
def error401(request):
    return render(request, 'accounts/error.html')

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customers.order_set.all()
    total_orders = orders.count()
    delivered = orders.filter(status ='Delivered').count()
    pending = orders.filter(status ='Pending').count()
    context  = {'orders':orders, 'total_orders':total_orders, 'delivered':delivered, 'pending':pending}
    return JsonResponse(context)
    #return render(request, 'accounts/user.html', context)


@login_required(login_url='login')
def aboutme(request):
    return render(request, 'accounts/aboutme.html')

@login_required(login_url='login')
def primarygoal(request):
    return render(request, 'accounts/goal.html')

@login_required(login_url='login')
def contactme(request):
    return render(request, 'accounts/contactme.html')

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customers,Order, fields = ('product', 'status'), extra = 4)
    customer = Customers.objects.get(id=pk)
    formset = OrderFormSet(queryset = Order.objects.none(),instance = customer)
    if request.method == 'POST':
        formset = OrderFormSet(request.POST,instance = customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context = {'formset':formset}
    return render(request, 'accounts/order_form.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance = order)
    
    if request.method == 'POST':
        form = OrderForm(request.POST, instance = order)
        if form.is_valid():
            form.save()
            return redirect('/')       
    context = {'formset':form}
    return render(request, 'accounts/order_form.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('/')
    context = {'item':order}
    return render(request, 'accounts/delete.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userSettings(request):
    customer = request.user.customers
    form = CustomerForm(instance = customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance = customer)
        if form.is_valid:
            form.save()
        
    context = {'form':form}
    return render (request,'accounts/account_settings.html', context)