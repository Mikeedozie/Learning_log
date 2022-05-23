from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Create your views here.
def login_view(request):
 
    users = User.objects.all()
        
    if request.method == 'POST':
        usern= request.POST['username']
        pass1 = request.POST['password']
                             
        myuser = authenticate(username=usern, password=pass1)
        if myuser is not None:
            login(request, myuser)
            return redirect('index')
        else:
            
            return redirect('login')
    return render(request, 'login.html')
    

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    if request.method != 'POST':
        form = UserCreationForm()
    else:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            registered_user = authenticate(username=new_user.username, password=request.POST['password1'])
            login(request, registered_user)
            return redirect('index')
        else:
            messages.error(request, "Bad Credentials")
            return redirect('register')
            
    context={'form':form}
    return render(request, 'register.html', context)
            
    