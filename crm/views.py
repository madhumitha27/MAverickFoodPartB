from pydoc import html

from django.contrib.auth import authenticate , login , update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse
from django.shortcuts import render , get_object_or_404 , redirect
from django.urls import reverse_lazy

from .models import *
from .forms import *
from django.db.models import Sum
from django.contrib import messages
from django.template.loader import get_template
from django.template import Context
import pdfkit

now = timezone.now()
def home(request):
   return render(request, 'crm/home.html',
                 {'crm': home})


@login_required
def customer_list(request):
    customer=Customer.objects.filter(created_date__lte=timezone.now())
    return render(request,'crm\customer_list.html',{'customers':customer})

def signup_view(request):
    success_url = reverse_lazy ( 'crm:home' )
    form = SignUpForm(request.POST)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect(success_url)
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def customer_edit(request,pk):
    customer = get_object_or_404 ( Customer , pk=pk )
    if request.method == "POST" :
        # update
        form = CustomerForm ( request.POST , instance=customer )
        if form.is_valid ( ) :
            print('check!!!!!!!!')
            customer = form.save ( commit=False )
            customer.updated_date = timezone.now ( )
            customer.save ( )
            customer = Customer.objects.filter ( created_date__lte=timezone.now ( ) )
            return render ( request , 'crm/customer_list.html' ,
                            {'customers' : customer} )
    else :
        # edit
        form = CustomerForm ( instance=customer )
    return render ( request , 'crm/customer_edit.html' , {'form' : form} )

@login_required
def customer_delete(request,pk):
    print(pk)
    customer = get_object_or_404 ( Customer , pk=pk )
    customer.delete ( )
    return redirect ( 'crm:customer_list' )
@login_required
def service_list(request):
   services = Service.objects.filter(created_date__lte=timezone.now())
   return render(request, 'crm/service_list.html', {'services': services})

@login_required
def service_new(request):
   if request.method == "POST":
       form = ServiceForm(request.POST)
       if form.is_valid():
           service = form.save(commit=False)
           service.created_date = timezone.now()
           service.save()
           services = Service.objects.filter(created_date__lte=timezone.now())
           return render(request, 'crm/service_list.html',
                         {'services': services})
   else:
       form = ServiceForm()
       # print("Else")
   return render(request, 'crm/service_new.html', {'form': form})

@login_required
def service_edit(request, pk):
   service = get_object_or_404(Service, pk=pk)
   if request.method == "POST":
       form = ServiceForm(request.POST, instance=service)
       if form.is_valid():
           service = form.save()
           # service.customer = service.id
           service.updated_date = timezone.now()
           service.save()
           services = Service.objects.filter(created_date__lte=timezone.now())
           return render(request, 'crm/service_list.html', {'services': services})
   else:
       # print("else")
       form = ServiceForm(instance=service)
   return render(request, 'crm/service_edit.html', {'form': form})

@login_required
def service_delete(request,pk):
    print(pk)
    service = get_object_or_404 ( Service , pk=pk )
    service.delete ( )
    return redirect ( 'crm:service_list' )

@login_required
def product_list(request):
   products = Product.objects.filter(created_date__lte=timezone.now())
   return render(request, 'crm/product_list.html', {'products': products})

@login_required
def product_new(request):
   if request.method == "POST":
       form = ProductForm(request.POST)
       if form.is_valid():
           product = form.save(commit=False)
           product.created_date = timezone.now()
           product.save()
           products = Product.objects.filter(created_date__lte=timezone.now())
           return render(request, 'crm/product_list.html',
                         {'products': products})
   else:
       form = ProductForm()
       # print("Else")
   return render(request, 'crm/product_new.html', {'form': form})

@login_required
def product_edit(request, pk):
   product = get_object_or_404(Product, pk=pk)
   if request.method == "POST":
       form = ProductForm(request.POST, instance=product)
       if form.is_valid():
           product = form.save()
           # service.customer = service.id
           product.updated_date = timezone.now()
           product.save()
           products = Product.objects.filter(created_date__lte=timezone.now())
           return render(request, 'crm/product_list.html', {'products': products})
   else:
       # print("else")
       form = ProductForm(instance=product)
   return render(request, 'crm/product_edit.html', {'form': form})

@login_required
def product_delete(request,pk):
    print(pk)
    product = get_object_or_404 ( Product , pk=pk )
    product.delete ( )
    return redirect ( 'crm:product_list' )
# Create your views here.


@login_required
def summary(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    customers = Customer.objects.filter(created_date__lte=timezone.now())
    services = Service.objects.filter(cust_name=pk)
    products = Product.objects.filter(cust_name=pk)
    sum_service_charge = Service.objects.filter(cust_name=pk).aggregate(Sum('service_charge'))
    sum_product_charge = Product.objects.filter(cust_name=pk).aggregate(Sum('charge'))
    return render ( request , 'crm/summary.html' , {'customers' : customers ,
                                                'products' : products ,
                                                'services' : services ,
                                                'sum_service_charge' : sum_service_charge ,
                                                'sum_product_charge' : sum_product_charge , } )