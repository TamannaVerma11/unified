from django.shortcuts import render
from django.http import *
from myAdmin.models import *
from . import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test

# Create your views here.

app_name = 'myAdmin'

def login_user(request):
    form = forms.LoginForm()
    message = ''
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        user = authenticate(
            username = request.POST['username'],
            password = request.POST['password']
        )
        if user is not None:
            login(request,user)
            return HttpResponseRedirect('/')
        else:
            message = 'Login Failed'
    return render(request, app_name+'\login.html', context={'form' : form, 'message' : message})

def signup_user(request):
    return render(request, app_name+"\signup.html")

@login_required(login_url='login_user')
def dashboard(request):
    return render(request, app_name+"\index.html")

@login_required(login_url='login_user')
def classIndex(request):
    class_form = forms.AddClassForm()
    section_form = forms.AddSectionForm()
    return render(request, app_name+"\classes\index.html", context={'class_form' : class_form, 'section_form' : section_form})

@login_required(login_url="login_user")
def addClass(request):
    return render(request, app_name+"\classes\addClass.html")

@login_required(login_url="login_user")
def addSection(request):
    return render(request, app_name+"\classes\addSection.html")