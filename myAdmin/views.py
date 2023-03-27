from django.shortcuts import render

# Create your views here.

app_name = 'myAdmin'

def dashboard(request):
    return render(request, app_name+"\index.html")

def login(request):
    return render(request, app_name+'\login.html')
