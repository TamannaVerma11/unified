from django.shortcuts import render
from django.http import *
from myAdmin.models import *
from . import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core import serializers
from django.contrib.auth.hashers import make_password
import requests

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
    sections = Section.objects.filter(created_by = request.user.id)
    classes = Class.objects.filter(created_by = request.user.id)
    class_section = ClassSection.objects.all()
    class_form = forms.AddClassForm()
    section_form = forms.AddSectionForm()
    if request.method == "POST":
        response_data = {}
        if request.POST.get('form_type')  == 'section':
            section_name = request.POST.get('section_name')
            created_by = request.user

            response_data['section_name'] = section_name

            Section.objects.create(
                section_name = section_name,
                created_by = created_by,
                )
        else:
            class_name = request.POST.get('class_name')
            sections = request.POST.getlist('section_id[]')
            created_by = request.user
            url = "https://lms.tabschool.in/app/api/add-class?name="+class_name+"&user_id="+str(request.user.id)
            headers={}
            requests.get(url,headers=headers)

            response_data['class_name'] = class_name
            response_data['section_id'] = sections

            add_class = Class.objects.create(
                class_name = class_name,
                created_by = created_by,
                )
            
            for section in sections:
                ClassSection.objects.create(
                    class_id_id  = add_class.id,
                    section_id_id = section
                )
        return JsonResponse({"response_data" : response_data}, status = 200)
    else:
        return render(request, app_name+"\classes\index.html", context={'class_form' : class_form, 'section_form' : section_form, 'sections' : sections, 'classes' : classes, 'class_section' : class_section})

@login_required(login_url='login_user')
def classDelete(request):
    class_data = Class.objects.get(adminbase_ptr_id  = request.POST.get('class_id'))
    class_data.delete()
    return JsonResponse({"message" : "Class deleted successfully"}, status = 200)

@login_required(login_url='login_user')
def studentIndex(request):
    class_data = Class.objects.filter(created_by = request.user.id)
    sections = Section.objects.filter(created_by = request.user.id)
    students = Student.objects.filter(created_by = request.user.id)
    if request.method == 'POST':
        user = User.objects.create(
            username = request.POST.get('first_name'),
            first_name = request.POST.get('first_name'),
            last_name = request.POST.get('last_name'),
            password = make_password("23wesdxc@#WESDXC%"),
            is_staff = 1,
            is_active = 1,
            is_superuser = 0,
        )

        parent = Parent.objects.create(
            mother_first_name = request.POST.get('mother_name'),
            mother_mobile = request.POST.get('mother_mobile'),
            father_first_name = request.POST.get('father_name'),
            father_mobile = request.POST.get('father_mobile'),
        )
        Student.objects.create(
            admission_no = request.POST.get('admission_no'),
            roll_no = request.POST.get('roll_no'),
            academic_year = request.POST.get('academic_year'),
            gender = request.POST.get('gender'),
            dob = request.POST.get('dob'),
            admission_data = request.POST.get('admission_data'),
            mobile = request.POST.get('father_mobile'),
            class_id_id  = request.POST.get('class_id'),
            created_by_id = request.user.id,
            parent_id_id = parent.id,
            address = request.POST.get('address'),
            user_id = user,
            section_id_id = request.POST.get('section_id'),
        )

    return render(request, app_name+"\students\student_add.html", context={'class_data' : class_data, 'sections' : sections, 'students' : students})

@login_required(login_url="login_user")
def teacherIndex(request):
    return render(request, app_name+"\/teachers\index.html")