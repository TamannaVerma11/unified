from django.shortcuts import render

# Create your views here.

app_name = 'myAdmin'

def dashboard(request):
    return render(request, "myAdmin/index.html")
