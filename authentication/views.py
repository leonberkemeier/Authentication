from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
from .forms import CreateUserForm


def home(request):
    return render(request, 'authentication/index.html')

#für alle die nicht ohne login zusehen sein sollen : @login_required(login_url='login') über der def einfügen
@login_required(login_url='login')
def inside(request):
    return render(request, 'authentication/inside.html')



# def signin(request):
    
#     return render(request, 'authentication/signin.html')

def loginPage(request):
    context={}  
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password = password)

            if user is not None:
                login(request, user)
                return redirect('inside')
        
            else:
                messages.info(request, 'Username OR Password is Incorrect')
                return render(request, 'authentication/login.html', context)

        
        return render(request, 'authentication/login.html', context)

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')

    else:

        form = CreateUserForm()

        if request.method =="POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
              form.save()
              user = form.clean_data.get('username')
              messages.success(request,'account was created for ' + user)

              return redirect('login')

    context = {'form': form}
    return render(request, "authentication/register.html", context)

def logoutUser(request):
    logout(request)
    return redirect ('login')




# def signout(request):
#     pass


# def registrationPage(request):
#     context = {}
#     return render(request, 'authentication/register.html', context)

# def loginPage(request):
#     context = {}
#     return render(request, 'authentication/login.html', context)