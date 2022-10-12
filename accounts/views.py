
import django
from django.shortcuts import redirect, render
from .utils import detectUser
from django.contrib.auth.decorators import login_required, user_passes_test

from vendor.forms import Vendorform
from .models import User,UserProfile
from.forms import Userform
from django.contrib import messages , auth

from django.core.exceptions import PermissionDenied

# Create your views here.

def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied
          

def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied

def registerUser(request):
    if request.method == 'POST':
        print(request.POST)
        form = Userform(request.POST)
        if form.is_valid():
            # password = form.cleaned_data['password']
            # user = form.save(commit=False)
            # user.set_password(password)
            # user.role =User.CUSTOMER
            # user.save()

            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
            user.role =User.CUSTOMER
            user.save()
            messages.success(request,'Your Accounts has been Registered Successfully!')
            return redirect('registerUser')
        else:
            print('invelete form')
            print(form.errors)
    else:
        form = Userform()
    context = {
        'form':form,
    }
    return render(request,'accounts/registerUser.html',context)

def registerVendor(request):
    if request.method == 'POST':
        # store the data
        form = Userform(request.POST)
        v_form = Vendorform(request.POST,request.FILES)
        if form.is_valid() and v_form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
            user.role =User.VENDOR
            user.save()
            vendor = v_form.save(commit = False)
            vendor.user=user
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()
            messages.success(request,'Your Accounts has been Registered Successfully! Please wait for approval')
            return redirect('registerVendor')
        else:
            print('invelete form')
            print(form.errors)
    else:
        form = Userform()
        v_form = Vendorform()
        context={
            'form':form,
            'v_form':v_form,
        }
    return render(request,'accounts/registerVendor.html',context)

def login(request):
    if request.user.is_authenticated:
        messages.warning(request,'Your are Logged in.')
        return redirect('myaccount')
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request,user)
            messages.success(request,'Your are Login Successfully!')
            return redirect('myaccount')
        else:
            messages.error(request,'Invailed login')
            return redirect('login')
    return render(request,'accounts/login.html')

def logout(request):
    auth.logout(request)
    messages.info(request,'you are logged out.')
    return redirect('login')

@login_required(login_url='login')
def myaccount(request):
    user = request.user
    # redirecturl = detectUser(user)
    return redirect(detectUser(user))

# def dashboard(request):
#     return render(request,'accounts/dashboard.html')
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    return render(request,'accounts/vendorDashboard.html')


@login_required(login_url='login')
@user_passes_test(check_role_customer)
def custDashboard(request):
    return render(request,'accounts/custDashboard.html')

