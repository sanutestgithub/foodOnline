from django.shortcuts import redirect, render
from .models import User
from.forms import Userform
from django.contrib import messages
# Create your views here.
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