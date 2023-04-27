from django.shortcuts import render, redirect
from django.http import *
from myAdmin.models import *
from . import forms
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.urls import reverse
from django.forms.models import model_to_dict
import requests
import json
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
        # lms_url = "https://lms.tabschool.in/app/api/login?email="+user.email+"&password="+request.POST['password']
        # lms_headers={}
        # lms_response = requests.get(lms_url,headers=lms_headers)
        # lms_response = json.loads(lms_response.text)
        # if lms_response['code'] == 100:
        #     SessionManager.objects.create(
        #         token = lms_response['token'],
        #         productType = 'lms',
        #         user = user
        #     )
        # ais_url = "https://ais.tabschool.in/api/login?email=Admin@tabschool.in&password=123456"
        # ais_headers={}
        # ais_response = requests.get(ais_url,headers=ais_headers)
        # ais_response = json.loads(ais_response.text)
        # if ais_response['success'] == True:
        #     SessionManager.objects.create(
        #         token = ais_response['data']['accessToken'],
        #         productType = 'ais',
        #         user = user
        #     )
        if user is not None:
            login(request,user)
            return HttpResponseRedirect('/dashboard')
        else:
            message = 'Login Failed'
    return render(request, app_name+'\login.html', context={'form' : form, 'message' : message})

def logout_user(request):
    SessionManager.objects.filter(user = request.user.id).delete()
    logout(request)
    return redirect('login_user')

def signup_user(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        mobile = request.POST.get('mobile_no')
        # url = "https://lms.tabschool.in/app/api/user-create?first_name="+first_name+"&last_name="+last_name+"&email="+email+"&password="+password+"&mobile="+mobile
        # headers={}
        # requests.get(url,headers=headers)
        user = User.objects.create(
            username = first_name+last_name,
            first_name = first_name,
            last_name = last_name,
            email = email,
            password = make_password(password),
            is_superuser = 0,
            is_staff = 1,
            is_active = 1
        )

        Profile.objects.create(
            plain_pass = password,
            mobile = mobile,
            user  = user
        )
        return render(request, app_name+"\school.html", {"user" : user})
    return render(request, app_name+"\signup.html")

def add_school(request):
    School.objects.create(
        school_name = request.POST.get('school'),
        role = request.POST.get('role'),
        learners = request.POST.get('learners'),
        mobile = request.POST.get('mobile'),
        email = request.POST.get('email'),
        user = User.objects.get(id = request.POST.get('user_id'))
    )

    user =  User.objects.get(id = request.POST.get('user_id'))

    return render(request, app_name+"\/address.html", {"user" : user})

def add_address(request):
    address = request.POST.get('address')
    city = request.POST.get('city')
    state = request.POST.get('state')
    pincode = request.POST.get('pincode')
    id = request.POST.get('user_id')

    Profile.objects.filter(id = id).update(
        address = address,
        city = city,
        state = state,
        pincode = pincode
    )
    user = User.objects.get(id = id)
    profile = Profile.objects.get(user = id)
    school = School.objects.get(user = id)

    url = "https://lms.tabschool.in/app/api/user-create"
    data = {
        'first_name': user.first_name, 
        'last_name': user.last_name, 
        'email': user.email, 
        'password': profile.plain_pass, 
        'mobile': profile.mobile, 
        'school_name': school.school_name, 
        'address': profile.address, 
        'school_email': school.email, 
        'school_mobile': school.mobile, 
        }
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    requests.post(url, data=json.dumps(data), headers=headers)
    return redirect("login_user")


@login_required(login_url='login_user')
def dashboard(request):
    return render(request, app_name+"\index.html")

@login_required(login_url='login_user')
def classIndex(request):
    sections = Section.objects.filter(creator = request.user.id)
    classes = Class.objects.filter(creator = request.user.id)
    class_section = ClassSection.objects.all()
    mediums = Medium.objects.filter(creator = request.user.id)
    class_form = forms.AddClassForm()
    if request.method == "POST":
        response_data = {}

        class_name = request.POST.get('class_name')
        sections = request.POST.getlist('section_id[]')
        medium = request.POST.get('medium')
        creator = request.user
        # medium_data = Medium.objects.get(id = medium)

        # lms_url = "https://lms.tabschool.in/app/api/add-class"
        # data = {
        #     'name' : class_name,
        #     'medium_id': medium_data.lms_id,
        #     }
        # data['section_id'] = []
        # for section in sections:
        #     section_data = Section.objects.get(adminbase_ptr_id = section)
        #     data['section_id'] = data['section_id'] + [section_data.lms_id]
        # lms_token = SessionManager.objects.get(user_id = request.user.id, productType = 'lms')
        # lms_headers = {'Content-type': 'application/json', 'Accept': 'text/plain',"Authorization":"Bearer "+lms_token.token}
        # lms_response = requests.post(lms_url, data=json.dumps(data), headers=lms_headers)
        # lms_response = json.loads(lms_response.text)
        # ais_url = "https://ais.tabschool.in/api/class-store"
        # ais_data = {
        #     'name' : class_name,
        #     }
        # ais_data['section_id'] = []
        # for section in sections:
        #     section_data = Section.objects.get(adminbase_ptr_id = section)
        #     ais_data['section_id'] = ais_data['section_id'] + [section_data.ais_id]
        # ais_token = SessionManager.objects.get(user_id = request.user.id, productType = 'ais')
        # ais_headers={'Content-type': 'application/json', 'Accept': 'text/plain',"Authorization":ais_token.token}
        # ais_response = requests.post(ais_url, data=json.dumps(ais_data), headers=ais_headers)
        # ais_response = json.loads(ais_response.text)
        response_data['class_name'] = class_name
        response_data['section_id'] = sections
        response_data['medium'] = medium
        
        add_class = Class.objects.create(
            class_name = class_name,
            creator = creator,
            medium = Medium.objects.get(id = medium),
            )
        
        for section in sections:
            ClassSection.objects.create(
                school_class  = add_class,
                section = Section.objects.get(id = section),
            )
        messages.success(request, 'Class added successfully')

    return render(request, app_name+"\classes\index.html", context={'class_form' : class_form, 'sections' : sections, 'classes' : classes, 'class_section' : class_section, 'mediums' : mediums})

@login_required(login_url='login_user')
def classDelete(request, id):
    class_data = Class.objects.get(id  = id)
    class_data.delete()
    messages.success(request, "Class deleted Successfully")
    return redirect('classIndex')

@login_required(login_url='login_user')
def classEdit(request, id):
    class_data = Class.objects.get(id = id)
    class_form = forms.AddClassForm(instance=class_data)
    sections = Section.objects.filter(creator = request.user.id)
    form_html = ''
    for form_data in class_form:
        form_html += '<div class="row mb-3"><label class="form-label col-sm-3 col-form-label">' + str(form_data.label) + ':</label><div class="col-sm-9">' + str(form_data) + '</div></div>'
    form_html += '<div class="row mb-3"><label class="form-label col-sm-3 col-form-label">Section:</label><div class="col-sm-9"><select class="form-control select" name="section_id[]" multiple>'
    for section in sections:
        selected = ''
        if ClassSection.objects.filter(section = section.id).count() > 0:
            selected = 'selected'
        form_html += '<option value="'+ str(section.id) +'" '+selected+'>'+ str(section.section_name) +'</option>'
    form_html += '</select></div></div>'
    return JsonResponse({'class_form' : form_html}, status = 200)

@login_required(login_url='login_user')
def classUpdate(request):
    if request.method == "POST":
        sections = request.POST.getlist('section_id[]')
        Class.objects.filter(id = request.POST.get('id')).update(
            class_name = request.POST.get('class_name'),
            medium = Medium.objects.get(id = request.POST.get('medium')),
            is_synced = 0
        )
        ClassSection.objects.filter(school_class = request.POST.get('id')).delete()
        for section in sections:
            ClassSection.objects.create(
                school_class  = Class.objects.get(id = request.POST.get('id')),
                section = Section.objects.get(id = section),
            )
        messages.success(request, 'Class updated successfully.')
    else:
        messages.error(request, 'Oops, Something went worng')
    return redirect('classIndex')

@login_required(login_url='login_user')
def mediumIndex(request):
    mediums = Medium.objects.filter(creator = request.user.id)
    medium_form = forms.AddMediumForm()
    if request.method == "POST":
        response_data = {}
        response_data['medium_name'] = request.POST.get('medium_name')
        # url = "https://lms.tabschool.in/app/api/add-medium?name="+request.POST.get('medium_name')
        # token = SessionManager.objects.get(user_id = request.user.id, productType='lms')
        # headers={"Authorization":"Bearer "+token.token}
        # response = requests.get(url,headers=headers)
        # response = json.loads(response.text)
        Medium.objects.create(
            medium_name = request.POST.get('medium_name'),
            creator = request.user
        )
        messages.success(request, 'Medium added successfully.')
    return render(request, app_name+"\medium\index.html", {"mediums" : mediums, "medium_form" : medium_form})

@login_required(login_url="login_user")
def mediumDelete(request, id):
    medium = Medium.objects.get(id = id)
    medium.delete()
    messages.success(request, "Medium deleted Successfully.")
    return redirect('mediumIndex')

@login_required(login_url='login_user')
def mediumEdit(request, id):
    medium = Medium.objects.get(id = id)
    medium_form = forms.AddMediumForm(instance=medium)
    form_html = ''
    for form_data in medium_form:
        form_html += '<div class="row mb-3"><label class="form-label col-sm-3 col-form-label">' + str(form_data.label) + ':</label><div class="col-sm-9">' + str(form_data) + '</div></div>'
    return JsonResponse({'medium_form' : form_html}, status = 200)

@login_required(login_url="login_user")
def mediumUpdate(request):
    if request.method == "POST":
        Medium.objects.filter(id = request.POST.get('id')).update(
            medium_name = request.POST.get('medium_name'),
            is_synced = 0
        )
        messages.success(request, 'Medium updated successfully.')
    else:
        messages.error(request, 'Oops, Something went worng')
    return redirect('mediumIndex')

@login_required(login_url='login_user')
def sectionIndex(request):
    sections = Section.objects.filter(creator = request.user.id)
    section_form = forms.AddSectionForm()
    if request.method == "POST":
        response_data = {}
        response_data['section_name'] = request.POST.get('section_name')
        # lms_url = "https://lms.tabschool.in/app/api/add-section?name="+request.POST.get('section_name')
        # lms_token = SessionManager.objects.get(user_id = request.user.id, productType = 'lms')
        # lms_headers={"Authorization":"Bearer "+lms_token.token}
        # lms_response = requests.get(lms_url,headers=lms_headers)
        # lms_response = json.loads(lms_response.text)
        # ais_url = "https://ais.tabschool.in/api/section-store?name="+request.POST.get('section_name')
        # ais_token = SessionManager.objects.get(user_id = request.user.id, productType = 'ais')
        # ais_headers={"Authorization":ais_token.token}
        # ais_response = requests.post(ais_url,headers=ais_headers)
        # ais_response = json.loads(ais_response.text)
        Section.objects.create(
            section_name = request.POST.get('section_name'),
            creator = request.user
        )
        messages.success(request, 'Section added successfully.')
    return render(request, app_name+"\section\index.html", {"sections" : sections, "section_form" : section_form})

@login_required(login_url="login_user")
def sectionDelete(request, id):
    section = Section.objects.get(id = id)
    section.delete()
    messages.success(request, "Section deleted Successfully")
    return redirect('sectionIndex')

@login_required(login_url='login_user')
def sectionEdit(request, id):
    section = Section.objects.get(id = id)
    section_form = forms.AddSectionForm(instance=section)
    form_html = ''
    for form_data in section_form:
        form_html += '<div class="row mb-3"><label class="form-label col-sm-3 col-form-label">' + str(form_data.label) + ':</label><div class="col-sm-9">' + str(form_data) + '</div></div>'
    return JsonResponse({'section_form' : form_html}, status = 200)

@login_required(login_url="login_url")
def sectionUpdate(request):
    if request.method == "POST":
        Section.objects.filter(id = request.POST.get('id')).update(
            section_name = request.POST.get('section_name'),
            is_synced = 0
        )
        messages.success(request, 'Section updated successfully')
    else:
        messages.error(request, 'Oops, Something went worng')
    return redirect('sectionIndex')

@login_required(login_url='login_user')
def categoryIndex(request):
    categories = Categories.objects.filter(creator = request.user.id)
    category_form = forms.AddCategoryForm()
    if request.method == "POST":
        response_data = {}
        response_data['category_name'] = request.POST.get('category_name')
        Categories.objects.create(
            category_name = request.POST.get('category_name'),
            creator = request.user
        )
        messages.success(request, 'Category added successfully.')
    return render(request, app_name+"\category\index.html", {"categories" : categories, "category_form" : category_form})

@login_required(login_url="login_user")
def categoryDelete(request, id):
    category = Categories.objects.get(id = id)
    category.delete()
    messages.success(request, "Category deleted Successfully")
    return redirect('categoryIndex')

@login_required(login_url='login_user')
def categoryEdit(request, id):
    category = Categories.objects.get(id = id)
    category_form = forms.AddCategoryForm(instance=category)
    form_html = ''
    for form_data in category_form:
        form_html += '<div class="row mb-3"><label class="form-label col-sm-3 col-form-label">' + str(form_data.label) + ':</label><div class="col-sm-9">' + str(form_data) + '</div></div>'
    return JsonResponse({'category_form' : form_html}, status = 200)

@login_required(login_url="login_url")
def categoryUpdate(request):
    if request.method == "POST":
        Categories.objects.filter(id = request.POST.get('id')).update(
            category_name = request.POST.get('category_name'),
            is_synced = 0
        )
        messages.success(request, 'Category updated successfully')
    else:
        messages.error(request, 'Oops, Something went worng')
    return redirect('categoryIndex')

@login_required(login_url='login_user')
def studentIndex(request):
    class_data = Class.objects.filter(creator = request.user.id)
    sections = Section.objects.filter(creator = request.user.id)
    students = Student.objects.filter(creator = request.user.id)
    categories = Categories.objects.filter(creator = request.user.id)
    if request.method == 'POST':
        # class_data_api = Class.objects.get(adminbase_ptr = request.POST.get('class_id'))
        # lms_url = "https://lms.tabschool.in/app/api/add-student"
        # data = {
        #     'father_first_name' : request.POST.get('father_name'),
        #     'father_mobile': request.POST.get('father_mobile'),
        #     'mother_first_name': request.POST.get('mother_name'),
        #     'mother_mobile': request.POST.get('mother_mobile'),
        #     'first_name': request.POST.get('first_name'),
        #     'last_name': request.POST.get('last_name'),
        #     'admission_no': request.POST.get('admission_no'),
        #     'gender': request.POST.get('gender'),
        #     'dob': request.POST.get('dob'),
        #     'current_address': request.POST.get('address'),
        #     'class_section_id': class_data_api.lms_id,
        #     'category_id': 1,
        #     'admission_no': request.POST.get('admission_no'),
        #     'admission_date': request.POST.get('admission_data'),
        #     'mother_email': request.POST.get('mother_email'),
        #     'father_email': request.POST.get('father_email'),
        #     }
        # lms_token = SessionManager.objects.get(user_id = request.user.id, productType = 'lms')
        # lms_headers = {'Content-type': 'application/json', 'Accept': 'text/plain',"Authorization":"Bearer "+lms_token.token}
        # lms_response = requests.post(lms_url, data=json.dumps(data), headers=lms_headers)
        # print(lms_response.text)
        # lms_response = json.loads(lms_response.text)
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
            mother_email = request.POST.get('mother_email'),
            father_first_name = request.POST.get('father_name'),
            father_email = request.POST.get('father_email'),
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
            school_class = Class.objects.get(id = request.POST.get('class_id')),
            creator_id = request.user.id,
            parent_id = parent.id,
            address = request.POST.get('address'),
            user_id = user.id,
            category = Categories.objects.get(id = request.POST.get('category_id')),
            section = Section.objects.get(id = request.POST.get('section_id')),
        )
        messages.success(request, 'Student added successfully.')
    return render(request, app_name+"\students\index.html", context={'class_data' : class_data, 'sections' : sections, 'students' : students, 'categories' : categories})

@login_required(login_url='login_user')
def studentDelete(request, id):
    student = Student.objects.get(id = id)
    Parent.objects.get(id = student.parent_id).delete()
    User.objects.get(id = student.user_id).delete()
    student.delete()
    messages.success(request, "Student deleted Successfully")
    return redirect('studentIndex')


@login_required(login_url="login_user")
def teacherIndex(request):
    return render(request, app_name+"\/teachers\index.html")

@login_required(login_url="login_user")
def departmentIndex(request):
    department = Department.objects.filter(created_by = request.user.id)
    if request.method == "POST":
        response_data = {}
        response_data['section_name'] = request.POST.get('section_name')
        lms_url = "https://lms.tabschool.in/app/api/add-section?name="+request.POST.get('section_name')
        lms_token = SessionManager.objects.get(user_id = request.user.id, productType = 'lms')
        lms_headers={"Authorization":"Bearer "+lms_token.token}
        lms_response = requests.get(lms_url,headers=lms_headers)
        lms_response = json.loads(lms_response.text)
        ais_url = "https://ais.tabschool.in/api/section-store?name="+request.POST.get('section_name')
        ais_token = SessionManager.objects.get(user_id = request.user.id, productType = 'ais')
        ais_headers={"Authorization":ais_token.token}
        ais_response = requests.post(ais_url,headers=ais_headers)
        ais_response = json.loads(ais_response.text)
        Section.objects.create(
            lms_id = lms_response['id'],
            ais_id = ais_response['data'],
            section_name = request.POST.get('section_name'),
            created_by = request.user
        )
        messages.success(request, 'Section added successfully')
    return render(request, app_name+"\section\index.html", {"sections" : sections, "section_form" : section_form})


@login_required(login_url="login_user")
def designationIndex(request):
    pass