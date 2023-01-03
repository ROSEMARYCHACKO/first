from ast import Or
from email import message
import email
from email.mime import image
from itertools import count
import os
from pyexpat.errors import messages
import re
from django.shortcuts import render, redirect, get_list_or_404
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.views.decorators.cache import cache_control
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
import datetime
from django.db.models import Q
import time
# Create your views here.

#login page 

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print("email : ",username, "password", password)
        admin = authenticate(username=username, password=password)
        if admin is not None:
            print("=-=-=-=-=admin verifyed-=-=-")
            request.session['admin'] = username
            request.session['user_type'] = "admin"
            return redirect('admin_home')
        
        else:
            service_provider_count = Service_provider.objects.filter(email=username, password=password).count()
            if service_provider_count > 0:
                request.session['service_provider'] = username
                request.session['user_type'] = "service_provider"
                print("=--=-=-serrvice provider login verifyed-=--=")
                return redirect('service_home')
            else:
                users_count = Users.objects.filter(email=username, password=password).count()
                if users_count > 0:
                    request.session['user'] = username
                    request.session['user_type'] = "user"
                    print("=-=-=-=-user login verifyed ")
                    return redirect('user_home')
                else:
                    print("=-=-=-login verification failed =-=-=")
                    messages.info(request,"Wrong username or password")
                    return redirect('/')
    return render(request,'index.html')


#admin home
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def admin_home(request):
    if 'admin' in request.session:
        print("=-=--=-admin home=-=-=-")
        return render(request,'admin_home.html')
    else:
        messages.info(request,"User not logged in")
        return redirect('/')

#admin add service provider
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def admin_add_serviceprovider(request):
    if 'admin' in request.session:
        print("=-=--=-admin add service provideer=-=-=-")
        if request.method == 'POST':
            email = request.POST.get('email')
            name = request.POST.get('name')
            password = request.POST.get('password')
            print("=-email, name , password-=",email,name,password)

            val = Service_provider.objects.filter(email=email,password=password)
            if val:
                messages.info(request, "This service provider already registered")
                return redirect(reverse('admin_add_serviceprovider'))
            else:
                service_provider = Service_provider(email=email,name=name,password=password)
                service_provider.save()
                messages.info(request, "Seccessfully registered")
                return redirect(reverse('admin_add_serviceprovider'))
        else:
            return render(request, 'add_service.html')
    else:
        messages.info(request,"User not logged in")
        return redirect('/')

#admin view service provider
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def admin_serviceprovider_view(request):
    if 'admin' in request.session:
        print("=-=--=-admin service provideer view=-=-=-")
        if request.method == 'POST':
            id = request.POST.get('id')
            print("=-=-id for delete =-=",id)
            delete_data = Service_provider.objects.get(id=id)
            delete_data.delete()
            messages.info(request,"Successfully deleted")
            
            return redirect(reverse('admin_serviceprovider_view'))
        else:
            all_data = Service_provider.objects.all().order_by('-id')
            print(all_data)
           
            return render(request, 'view_service.html', { 'all_data' : all_data })
    else:
        messages.info(request,"User not logged in")
        return redirect('/')

#admin edit service provider
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def admin_serviceprovider_edit(request):
    if 'admin' in request.session:
        
        print("=-=--=-admin service provideer edit=-=-=-")
        id = request.GET.get('id')
        print("=-=-id for edit=-=-=",id)
        if request.method == 'POST':
            email = request.POST.get('email')
            name = request.POST.get('name')
            password = request.POST.get('password')
            print("=-email, name , password-=",email,name,password)
            query = Service_provider.objects.filter(id=id).update(name=name,email=email,password=password)
            if query:
                messages.info(request,"Successfully edited")
            else:
                messages.info(request,"Something went wrong")
            
            return redirect(reverse('admin_serviceprovider_view'))
        else:
            
            try:
                all_data = Service_provider.objects.get(id=id)
           
                return render(request, 'edit_service.html', { 'all_data' : all_data })
            except ObjectDoesNotExist:
                return render(request, 'edit_service.html')
    else:
        messages.info(request,"User not logged in")
        return redirect('/')


#admin logout
def logout_admin(request):
    try:
        del request.session['admin']
        request.session.set_expiry(0.0001)
        return redirect('/')
    except KeyError:
        messages.info(request,"User not logged in")
        return redirect('/')


#service provider home
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def service_home(request):
    if 'service_provider' in request.session:
        print("=-=--=-service_provider home=-=-=-")
        return render(request,'service_provider_home.html')
    else:
        messages.info(request,"User not logged in")
        return redirect('/')

#add products 
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def add_products(request):
    if 'service_provider' in request.session:
        if request.method == 'POST':
            print("=-=--=add products=-=-=")
            name = request.POST.get('name')
            des =  request.POST.get('des')
            rate = request.POST.get('rate')
            count = request.POST.get('count')
            images = request.FILES.get('file')
            #getting extension of file
            ext = images.name.split('.')[-1]
            print("=-=-=-ext=-=-=-",ext)
            images.name = datetime.now().strftime('%Y%m%d%H%M%S')+"."+ext
            print("-=-=-image new name=-=-", images.name)

            if not Products.objects.filter(name=name).exists():
                Products.objects.create(name=name,description=des,rate=rate,count=count,image=images)
                messages.info(request,"Prodct added successfully")
                return redirect(reverse('service_provider_product_view'))
            else:
                messages.info(request,"Prodct allready exists")
                return redirect(reverse('add_products'))
                

        else:
            print("=-=--=-service_provider add_products=-=-=-")
            return render(request,'add_products.html')
    else:
        messages.info(request,"User not logged in")
        return redirect('/')

#service_provider_product_view
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def service_provider_product_view(request):
    if 'service_provider' in request.session:
        print("=-=--=-View product service provider=-=-=-")
        if request.method == 'POST':
            id = request.POST.get('id')
            print("=-=-id for delete =-=",id)
            delete_data = Products.objects.get(id=id)
            
            os.remove(delete_data.image.path)
            delete_data.delete()
            messages.info(request,"Successfully deleted")
            
            return redirect(reverse('service_provider_product_view'))
        else:

            all_data = Products.objects.all().order_by('-id')
            print(all_data)
            return render(request,'service_provider_product_view.html',{'all_data':all_data})
    else:
        messages.info(request,"User not logged in")
        return redirect('/')

#service provider edit product
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def service_provider_product_edit(request):
    if 'service_provider' in request.session:
        id = request.GET.get('id')
        print("=-=--=-edit product service provider=-=-=-")
        if request.method == 'POST':
            name = request.POST.get('name')
            des = request.POST.get('des')
            rate = request.POST.get('rate')
            count = request.POST.get('count')
            query = Products.objects.filter(id=id).update(name=name,description=des,rate=rate,count=count)
            if query:
                messages.info(request,"Successfully edited")
            else:
                messages.info(request,"Something went wrong")
            
            return redirect(reverse('service_provider_product_view'))
        else:

            all_data = Products.objects.get(id=id)
            print(all_data)
            return render(request,'service_provider_product_edit.html',{'all_data':all_data})
    else:
        messages.info(request,"User not logged in")
        return redirect('/')


#service provider order view
def service_provider_order_view(request):
    if 'service_provider' in request.session:
        print("=-=--=-service provider order view=-=-=-")
        if request.method == 'POST':
            print("=-=-=-= order comfiration=-=-=-=")
            id = request.POST.get('id')
            order = Order.objects.filter(id=id).update(status="Placed",service_provider=request.session['service_provider'])
            
            messages.info(request, "Seccessfully ordered")
            return redirect(reverse('service_provider_order_view'))

        else:

            all_data = Order.objects.filter(status = "Ordered")
            print(all_data)
            return render(request,'service_provider_order_view.html',{'all_data':all_data})
    else:
        messages.info(request,"User not logged in")
        return redirect('/')
    
#service provider history
def service_provider_order_history(request):
    if 'service_provider' in request.session:

        all_data = Order.objects.filter(status = "Placed")
        print(all_data)
        return render(request,'service_provider_order_history.html',{'all_data':all_data})
    else:
        messages.info(request,"User not logged in")
        return redirect('/')

#service provider logout
def logout_service_provider(request):
    try:
        del request.session['service_provider']
        request.session.set_expiry(0.0001)
        return redirect('/')
    except KeyError:
        messages.info(request,"User not logged in")
        return redirect('/')

#service privde soil test details
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def service_provider_soil(request):
    if 'service_provider' in request.session:
        if request.method == 'POST':
            if 'accept' in request.POST:
                print("Accept")
                id = request.POST.get('id')
                comment = request.POST.get('accept')
                update = Soil_test.objects.filter(id=id).update(comment=comment,status="ACCEPTED")
                
                messages.info(request, "Seccessfully accepted")
                return redirect(reverse('service_provider_soil'))
            else:
                print("Compleated")
                id = request.POST.get('id')
                comment = request.POST.get('comment')
                report = request.POST.get('report')
                if report == "":
                    messages.info(request, "Need report..!")
                    return redirect(reverse('service_provider_soil'))
                else:
                    update = Soil_test.objects.filter(id=id).update(comment=comment,status="COMPLETED",flag=0,results=report)
                    
                    messages.info(request, "Seccessfully completed")
                    return redirect(reverse('service_provider_soil'))
            
        else:
            serrvice_provider = Service_provider.objects.get(email=request.session['service_provider'])
            all_data = Soil_test.objects.filter(service_provider_id=serrvice_provider.id,flag=1).all()
            print(all_data)
            return render(request,'service_provider_soil_request.html',{'all_data':all_data})
    else:
        messages.info(request,"User not logged in")
        return redirect('/')

#=-=-=-=-user section=--=-=-

#user register

def user_register(request):
        if request.method == 'POST':
            email = request.POST.get('email')
            name = request.POST.get('name')
            password = request.POST.get('password')
            ph = request.POST.get('ph')
            address = request.POST.get('address')
            print("=-email, name , password, ph, address-=",email,name,password,ph,address)

            val = Users.objects.filter(email=email)
            if val:
                messages.info(request, "This Email already registered")
                return redirect(reverse('user_register'))
            else:
                users = Users(email=email,name=name,password=password,address=address,phone=ph)
                users.save()
                messages.info(request, "Seccessfully registered")
                return redirect(reverse('login'))
        else:
            return render(request, 'user_register.html')

#user home
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def user_home(request):
    if 'user' in request.session:
        print("=-=--=-user home=-=-=-")
        if request.method == 'POST':
            print("=---purchase=-=-=-")
            id = request.POST.get('id')
            item_count = request.POST.get('count')
            query = Products.objects.get(id=id)
            name = query.name
            description = query.description
            rate = query.rate
            count = query.count
            image = query.image
            print("=-=-name=-=-=",name)
            if int(item_count) > int(count):
                print("=-=-=-large=-=-")
                messages.info(request,"Out of stock")
                return redirect(reverse('user_home'))
            else:
                date = datetime.datetime.now().strftime ("%Y-%m-%d")
                user_filter = Users.objects.get(email = request.session['user'])
                total_rate = int(item_count) * int(rate)
                new_product_count = int(count) - int(item_count)
                purchase = Order(name=name,user_id=user_filter.id,rate=total_rate,count = item_count,image = image,service_provider = "",status = "Ordered",date = date)
                poroducts = Products.objects.filter(id=id).update(count=new_product_count)
                purchase.save()
                messages.info(request, "Seccessfully delivered")
                return redirect(reverse('user_home'))
        else:
            all_data = Products.objects.all().order_by('-id')
            print(all_data)
            return render(request,'user_home.html',{'all_data':all_data})
    else:
        
        messages.info(request,"User not logged in")
        return redirect('/')

#view order by users
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def view_orders_user(request):
    if 'user' in request.session:
        print("=-=--=-user order view=-=-=-")
        if request.method == 'POST':
            print("=---cancel order=-=-=-")
            id = request.POST.get('id')
            order = Order.objects.get(id=id)
            order_update = Order.objects.filter(id=id).update(status="canceled")
            product = Products.objects.get(name = order.name)
            count = int(product.count) + int(order.count)
            product_update = Products.objects.filter(name=order.name).update(count = count)
            messages.info(request,"Order canceld")
            return redirect(reverse('view_orders_user'))
            
        else:
            user = Users.objects.get(email = request.session['user'])
            all_data = Order.objects.filter(Q(status="Ordered",user_id=user.id) | Q(status="delivered",user_id=user.id)).order_by('-id')
            print(all_data)
            return render(request,'user_order_view.html',{'all_data':all_data})
    else:
        
        messages.info(request,"User not logged in")
        return redirect('/')

#user order history
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def history_orders_user(request):
    if 'user' in request.session:
        print("=-=--=-user order history=-=-=-")
        
        
        user = Users.objects.get(email = request.session['user'])
        all_data = Order.objects.filter(~Q(status = "Ordered"),user_id=user.id).order_by('-id')
        print(all_data)
        return render(request,'history_orders_user.html',{'all_data':all_data})
    else:
        
        messages.info(request,"User not logged in")
        return redirect('/')

  
#user provider logout
def logout_user(request):
    try:
        del request.session['user']
        request.session.set_expiry(0.0001)
        return redirect('/')
    except KeyError:
        messages.info(request,"User not logged in")
        return redirect('/')

#chat section
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def chat_section(request):
    if request.session['user_type'] == "user" :
        print("=-=-= user type-=-=",request.session['user_type'])
        
        if request.method == 'POST':
            print("=-=-=- send=-=-=-")
            chat = request.POST.get('chat')
                # get current time
            date_time = datetime.datetime.now().strftime ("%Y-%m-%d")
            # product = Products.objects.get(id=id)
            current_user_id = Users.objects.get(email=request.session['user'])
            add = Chat(user_type="user",user_name=current_user_id.name,user_id=current_user_id.id,comment=chat,status=1,date=date_time)
            add.save()
            return redirect(reverse('chat_section'))
        else:
            print("=-=--=-chat_section user=-=-=-")
            chat = Chat.objects.filter(status = 1)
            # product = Products.objects.filter(id=id)
            current_user_id = Users.objects.get(email=request.session['user'])
            return render(request,'comment.html',{'chat':chat,'user_id':current_user_id.id,'user_name':current_user_id.name})

        
    else:
        if request.session['user_type'] == "service_provider":
            print("=-=-=-= chat_section service provideer")
            
            if request.method == 'POST':
                print("=-=-=- send=-=-=-")
                chat = request.POST.get('chat')
                # get current time
                date_time = datetime.datetime.now().strftime ("%Y-%m-%d")
                # product = Products.objects.get(id=id)
                current_user_id = Service_provider.objects.get(email=request.session['service_provider'])
                add = Chat(user_type="service_provider",user_name=current_user_id.name,user_id=current_user_id.id,comment=chat,status=1,date=date_time)
                add.save()
                return redirect(reverse('chat_section'))

            else:
                print("=-=--=-chat_section user=-=-=-")
                chat = Chat.objects.filter(status = 1)
                # product = Products.objects.filter(id=id)
                current_user_id = Service_provider.objects.get(email=request.session['service_provider'])
                print("=-=-=user name=-=-",current_user_id.name)
                print("=-=-=user id=-=-",current_user_id.id)
                return render(request,'comment.html',{'chat':chat,'user_id':current_user_id.id,'user_name':current_user_id.name})
        else:
            messages.info(request,"User not logged in")
            return redirect('/')

#user soil test
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def user_soil(request):
    if 'user' in request.session:
        print("=-=-=-user soil test request =-=-=-")
        if request.method == 'POST':
            print("=-=-=- send request=-=-=-")
            id = request.POST.get('id')
            message = request.POST.get('message')
            print("==-=-id=-=-",id)
            print("=-=-message=-=-", message)
            date_time = datetime.datetime.now().strftime ("%Y-%m-%d")
            serrvice_provider = Service_provider.objects.get(id=id)
            user = Users.objects.get(email = request.session['user'])
            soil = Soil_test(user_name=user.name,user_id=user.id,comment=message,service_provider=serrvice_provider.name,service_provider_id=serrvice_provider.id,results="",status='REQUESTED',date=date_time,flag=1)
            soil.save()
            return redirect(reverse('user_soil'))
        else:
            user = Users.objects.get(email = request.session['user'])
            query = Soil_test.objects.filter(user_name=user.name,flag=1).count()
            if query < 1:
                all_data = Service_provider.objects.all().order_by('-id')
                return render(request, "user_soil.html",{'all_data':all_data})
            else:
                is_active = Soil_test.objects.get(user_name=user.name,flag=1)
                return render(request, "user_soil.html",{'is_active':is_active})
    else:
        
        messages.info(request,"User not logged in")
        return redirect('/')
    
    #user soil test history
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def user_soil_history(request):
    if 'user' in request.session:
        if request.method == 'POST':
            id = request.POST.get('id')
            print("=-=-=- download pdf=-=-=-")
            all_data = Soil_test.objects.get(id=id)
            return render(request, "dwonload_pdf.html",{'all_data':all_data})
        else:
            
            user = Users.objects.get(email = request.session['user'])
            query = Soil_test.objects.filter(user_name=user.name,flag=0).count()
            if query < 1:
                return render(request, "user_soil_history.html",)
            else:
                all_data = Soil_test.objects.filter(user_name=user.name,flag=0).all()
                return render(request, "user_soil_history.html",{'all_data':all_data})
    else:
            
        messages.info(request,"User not logged in")
        return redirect('/')



