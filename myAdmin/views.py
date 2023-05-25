from django.shortcuts import render, redirect
from django.http import *
from myAdmin.models import *
from . import forms
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib import messages
import requests
import json
import pandas as pd
import os
from django.core.files.storage import FileSystemStorage
from myAdmin.otp import verify_otp
# Create your views here.

app_name = 'myAdmin'

def login_user(request):
    form = forms.LoginForm()
    message = ''
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        authenticate(
            email = request.POST['email'],
            password = request.POST['password']
        )
        user = User.objects.get(email = request.POST['email'])
        lms_url = "https://lms.tabschool.in/app/api/login?email="+user.email+"&password="+request.POST['password']
        lms_headers={}
        lms_response = requests.get(lms_url,headers=lms_headers)
        lms_response = json.loads(lms_response.text)
        if lms_response['code'] == 100:
            SessionManager.objects.create(
                token = lms_response['token'],
                productType = 'lms',
                user = user
            )
        ais_url = "https://ais.tabschool.in/api/login?email=Admin@tabschool.in&password=123456"
        ais_headers={}
        ais_response = requests.get(ais_url,headers=ais_headers)
        ais_response = json.loads(ais_response.text)
        if ais_response['success'] == True:
            SessionManager.objects.create(
                token = ais_response['data']['accessToken'],
                productType = 'ais',
                user = user
            )
        if user is not None:
            login(request,user)
            return HttpResponseRedirect('/dashboard')
        else:
            message = 'Login Failed'
    return render(request, app_name+'/login.html', context={'form' : form, 'message' : message})

def logout_user(request):
    SessionManager.objects.filter(user = request.user.id).delete()
    logout(request)
    return redirect('login_user')

def signup_user(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = '23wesdxc@#WESDXC%'
        mobile = request.POST.get('mobile_no')
        otp = request.POST.get('otp')
        if verify_otp(mobile, otp):
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
            return render(request, app_name+"/password.html", {"user" : user})
        else:
            messages.error(request, 'Invalid OTP')
    return render(request, app_name+"/signup.html")

def add_password(request):
    user = User.objects.get(id = request.POST.get('user_id'))
    User.objects.filter(id = request.POST.get('user_id')).update(
        password = make_password(request.POST.get('password'))
    )
    return render(request, app_name+"/school.html", {"user" : user})

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

    return render(request, app_name+"/address.html", {"user" : user})

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

    bus_url = "https://tracking.tabschool.in/api/school-store"
    bus_data = {
        'name': user.first_name, 
        'email': user.email, 
        'tel_number': profile.mobile, 
        'password' : profile.plain_pass
        }
    bus_headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    requests.post(bus_url, data=json.dumps(bus_data), headers=bus_headers)
    lms_url = "https://lms.tabschool.in/app/api/user-create"
    lms_data = {
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
    lms_headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    requests.post(lms_url, data=json.dumps(lms_data), headers=lms_headers)
    return redirect("login_user")

@login_required(login_url='login_user')
def dashboard(request):
    school_class = Class.objects.filter(creator = request.user.id)
    school_class_count = Class.objects.filter(creator = request.user.id).count()
    student = Student.objects.filter(creator = request.user.id)
    student_count = Student.objects.filter(creator = request.user.id).count()
    teacher = Teacher.objects.filter(creator = request.user.id)
    teacher_count = Teacher.objects.filter(creator = request.user.id).count()
    return render(request, app_name+"/index.html", {'school_class' : school_class, 'student' : student, 'teacher' : teacher, 'school_class_count' : school_class_count, 'student_count' : student_count, 'teacher_count' : teacher_count})

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

    return render(request, app_name+"/classes/index.html", context={'class_form' : class_form, 'sections' : sections, 'classes' : classes, 'class_section' : class_section, 'mediums' : mediums})

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

@login_required(login_url="login_user")
def classSync(request, id):
    school_class =  Class.objects.get(id = id)
    sections  = ClassSection.objects.filter(school_class = id)
    lms_url = "https://lms.tabschool.in/app/api/add-class"
    data = {
        'name' : school_class.class_name,
        'medium_id': school_class.medium.id,
        }
    data['section_id'] = []
    for section in sections:
        section_data = Section.objects.get(id = section.section_id)
        data['section_id'] = data['section_id'] + [section_data.id]
    lms_token = SessionManager.objects.get(user_id = request.user.id, productType = 'lms')
    lms_headers = {'Content-type': 'application/json', 'Accept': 'text/plain',"Authorization":"Bearer "+lms_token.token}
    lms_response = requests.post(lms_url, data=json.dumps(data), headers=lms_headers)
    lms_response = json.loads(lms_response.text)
    ais_url = "https://ais.tabschool.in/api/class-store"
    ais_data = {
        'name' : school_class.class_name,
        }
    ais_data['section_id'] = []
    for section in sections:
        section_data = Section.objects.get(id = section.section_id)
        ais_data['section_id'] = ais_data['section_id'] + [section_data.id]
    ais_token = SessionManager.objects.get(user_id = request.user.id, productType = 'ais')
    ais_headers={'Content-type': 'application/json', 'Accept': 'text/plain',"Authorization":ais_token.token}
    ais_response = requests.post(ais_url, data=json.dumps(ais_data), headers=ais_headers)
    ais_response = json.loads(ais_response.text)
    if lms_response['status'] == 'success':
        Class.objects.filter(id = id).update(is_synced = 1)
        return JsonResponse({'status' : 'success'}, status = 200)
    else:
        return JsonResponse({'status' : 'error'}, status = 200)

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
    return render(request, app_name+"/medium/index.html", {"mediums" : mediums, "medium_form" : medium_form})

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

@login_required(login_url="login_user")
def mediumSync(request, id):
    medium = Medium.objects.get(id = id)
    url = "https://lms.tabschool.in/app/api/add-medium?name="+medium.medium_name
    token = SessionManager.objects.get(user_id = request.user.id, productType='lms')
    headers={"Authorization":"Bearer "+token.token}
    response = requests.get(url,headers=headers)
    print(response)
    response = json.loads(response.text)
    if response['status'] == 'success':
        Medium.objects.filter(id = id).update(is_synced = 1)
        return JsonResponse({'status' : 'success'}, status = 200)
    else:
        return JsonResponse({'status' : 'error'}, status = 200)

@login_required(login_url='login_user')
def sectionIndex(request):
    sections = Section.objects.filter(creator = request.user.id)
    section_form = forms.AddSectionForm()
    if request.method == "POST":
        response_data = {}
        response_data['section_name'] = request.POST.get('section_name')
        Section.objects.create(
            section_name = request.POST.get('section_name'),
            creator = request.user
        )
        messages.success(request, 'Section added successfully.')
    return render(request, app_name+"/section/index.html", {"sections" : sections, "section_form" : section_form})

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

@login_required(login_url="login_user")
def sectionSync(request, id):
    section = Section.objects.get(id = id)
    lms_url = "https://lms.tabschool.in/app/api/add-section?name="+section.section_name
    lms_token = SessionManager.objects.get(user_id = request.user.id, productType = 'lms')
    lms_headers={"Authorization":"Bearer "+lms_token.token}
    lms_response = requests.get(lms_url,headers=lms_headers)
    lms_response = json.loads(lms_response.text)
    ais_url = "https://ais.tabschool.in/api/section-store?name="+section.section_name
    ais_token = SessionManager.objects.get(user_id = request.user.id, productType = 'ais')
    ais_headers={"Authorization":ais_token.token}
    ais_response = requests.post(ais_url,headers=ais_headers)
    ais_response = json.loads(ais_response.text)
    if lms_response['status'] == 'success':
        Section.objects.filter(id = id).update(is_synced = 1)
        return JsonResponse({'status' : 'success'}, status = 200)
    else:
        return JsonResponse({'status' : 'error'}, status = 200)

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
    return render(request, app_name+"/category/index.html", {"categories" : categories, "category_form" : category_form})

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

@login_required(login_url="login_user")
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

@login_required(login_url="login_user")
def categorySync(request, id):
    category = Categories.objects.get(id = id)
    url = "https://lms.tabschool.in/app/api/add-category?name="+category.category_name
    token = SessionManager.objects.get(user_id = request.user.id, productType='lms')
    headers={"Authorization":"Bearer "+token.token}
    response = requests.get(url,headers=headers)
    print(response)
    response = json.loads(response.text)
    if response['status'] == 'success':
        Categories.objects.filter(id = id).update(is_synced = 1)
        return JsonResponse({'status' : 'success'}, status = 200)
    else:
        return JsonResponse({'status' : 'error'}, status = 200)

@login_required(login_url='login_user')
def studentIndex(request):
    class_data = Class.objects.filter(creator = request.user.id)
    sections = Section.objects.filter(creator = request.user.id)
    students = Student.objects.filter(creator = request.user.id)
    categories = Categories.objects.filter(creator = request.user.id)
    student_form = forms.AddStudentForm()
    parent_form = forms.AddParentForm()
    bulk_student_form = forms.BulkStudentUploadForm()
    student_user_form = forms.AddStudentUserForm()
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
            mother_first_name = request.POST.get('mother_first_name'),
            mother_mobile = request.POST.get('mother_mobile'),
            mother_email = request.POST.get('mother_email'),
            father_first_name = request.POST.get('father_first_name'),
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
            school_class = Class.objects.get(id = request.POST.get('school_class')),
            creator_id = request.user.id,
            parent_id = parent.id,
            address = request.POST.get('address'),
            user_id = user.id,
            category = Categories.objects.get(id = request.POST.get('category')),
            section = Section.objects.get(id = request.POST.get('section')),
        )
        messages.success(request, 'Student added successfully.')
    return render(request, app_name+"/students/index.html", context={'class_data' : class_data, 'sections' : sections, 'students' : students, 'categories' : categories, 'student_form' : student_form, 'parent_form' : parent_form, 'student_user_form' : student_user_form, 'bulk_student_form' : bulk_student_form})

@login_required(login_url='login_user')
def studentDelete(request, id):
    student = Student.objects.get(id = id)
    Parent.objects.get(id = student.parent_id).delete()
    User.objects.get(id = student.user_id).delete()
    student.delete()
    messages.success(request, "Student deleted Successfully")
    return redirect('studentIndex')

@login_required(login_url="login_user")
def studentEdit(request, id):
    student = Student.objects.get(id = id)
    user = User.objects.get(id = student.user.id)
    parent = Parent.objects.get(id = student.parent.id)
    student_form = forms.AddStudentForm(instance=student)
    parent_form = forms.AddParentForm(instance=parent)
    student_user_form = forms.AddStudentUserForm(instance=user)
    form_html = '<div class="row mb-3"><div class="col-md-4"><label class="form-label" for="admission_no">' + str(student_form.fields['admission_no'].label) + '</label>' + str(student_form['admission_no']) + '</div><div class="col-md-2"><label class="form-label" for="roll_no">' + str(student_form.fields['roll_no'].label) + '</label>' + str(student_form['roll_no']) + '</div><div class="col-md-2"><label class="form-label" for="class_id">' + str(student_form.fields['school_class'].label) + '</label>' + str(student_form['school_class']) + '</div><div class="col-md-2"><label class="form-label" for="section_id">' + str(student_form.fields['section'].label) + '</label>' + str(student_form['section']) + '</div><div class="col-md-2"><label class="form-label" for="academic_year">' + str(student_form.fields['academic_year'].label) + '</label>' + str(student_form['academic_year']) + '</div></div><div class="row mb-3"><div class="col-md-6"><label class="form-label" for="first_name">' + str(student_user_form.fields['first_name'].label) + '</label>' + str(student_user_form['first_name']) + '</div><div class="col-md-6"><label class="form-label" for="last_name">' + str(student_user_form.fields['last_name'].label) + '</label>' + str(student_user_form['last_name']) + '</div></div><div class="row mb-3"><div class="col-md-3"><label class="form-label" for="gender">' + str(student_form.fields['gender'].label) + '</label>' + str(student_form['gender']) + '</div><div class="col-md-3"><label class="form-label" for="dob">' + str(student_form.fields['dob'].label) + '</label>' + str(student_form['dob']) + '</div><div class="col-md-3"><label class="form-label" for="admission_data">' + str(student_form.fields['admission_data'].label) + '</label>' + str(student_form['admission_data']) + '</div><div class="col-md-3"><label class="form-label" for="admission_data">' + str(student_form.fields['category'].label) + '</label>' + str(student_form['category']) + '</div></div><div class="row mb-3"><div class="col-md-6"><label class="form-label" for="father_first_name">' + str(parent_form.fields['father_first_name'].label) + '</label>' + str(parent_form['father_first_name']) + '</div><div class="col-md-6"><label class="form-label" for="mother_first_name">' + str(parent_form.fields['mother_first_name'].label) + '</label>' + str(parent_form['mother_first_name']) + '</div></div><div class="row mb-3"><div class="col-md-6"><label class="form-label" for="father_mobile">' + str(parent_form.fields['father_mobile'].label) + '</label>' + str(parent_form['father_mobile']) + '</div><div class="col-md-6"><label class="form-label" for="mother_mobile">' + str(parent_form.fields['mother_mobile'].label) + '</label>' + str(parent_form['mother_mobile']) + '</div></div><div class="row mb-3"><div class="col-md-6"><label class="form-label" for="father_email">' + str(parent_form.fields['father_email'].label) + '</label>' + str(parent_form['father_email']) + '</div><div class="col-md-6"><label class="form-label" for="mother_email">' + str(parent_form.fields['mother_email'].label) + '</label>' + str(parent_form['mother_email']) + '</div></div><div class="row mb-3"><div class="col-md-12"><label class="form-label" for="address">' + str(student_form.fields['address'].label) + '</label>' + str(student_form['address']) + '</div></div>'
    return JsonResponse({'student_form' : form_html}, status = 200)

@login_required(login_url="login_user")
def studentUpdate(request):
    if request.method == "POST":
        student = Student.objects.get(id = request.POST.get('id'))
        Student.objects.filter(id = request.POST.get('id')).update(
            admission_no = request.POST.get('admission_no'),
            roll_no = request.POST.get('roll_no'),
            academic_year = request.POST.get('academic_year'),
            gender = request.POST.get('gender'),
            dob = request.POST.get('dob'),
            admission_data = request.POST.get('admission_data'),
            mobile = request.POST.get('father_mobile'),
            school_class = Class.objects.get(id = request.POST.get('school_class')),
            creator_id = request.user.id,
            address = request.POST.get('address'),
            category = Categories.objects.get(id = request.POST.get('category')),
            section = Section.objects.get(id = request.POST.get('section')),
        )
        User.objects.filter(id = student.user.id).update(
            username = request.POST.get('first_name'),
            first_name = request.POST.get('first_name'),
            last_name = request.POST.get('last_name'),
        )

        Parent.objects.filter(id = student.parent.id).update(
            mother_first_name = request.POST.get('mother_first_name'),
            mother_mobile = request.POST.get('mother_mobile'),
            mother_email = request.POST.get('mother_email'),
            father_first_name = request.POST.get('father_first_name'),
            father_email = request.POST.get('father_email'),
            father_mobile = request.POST.get('father_mobile'),
        )
        
        messages.success(request, 'Student updated successfully')
    else:
        messages.error(request, 'Oops, Something went worng')
    return redirect('studentIndex')

@login_required(login_url="login_user")
def studentSync(request, id):
    student = Student.objects.get(id = id)
    parent = Parent.objects.get(id = student.parent.id)
    student_user = User.objects.get(id = student.user.id)
    lms_url = "https://lms.tabschool.in/app/api/add-student"
    data = {
        'father_first_name' : parent.father_first_name,
        'father_mobile': parent.father_mobile,
        'mother_first_name': parent.mother_first_name,
        'mother_mobile': parent.mother_mobile,
        'first_name': student_user.first_name,
        'last_name': student_user.last_name,
        'admission_no': student.admission_no,
        'gender': student.gender,
        'dob': student.dob,
        'current_address': student.address,
        'class_section_id': student.school_class.id ,
        'category_id': student.category.id,
        'mother_email': parent.mother_email,
        'father_email': parent.father_email,
        }
    lms_token = SessionManager.objects.get(user_id = request.user.id, productType = 'lms')
    lms_headers = {'Content-type': 'application/json', 'Accept': 'text/plain',"Authorization":"Bearer "+lms_token.token}
    lms_response = requests.post(lms_url, data=json.dumps(data, indent=4, sort_keys=True, default=str), headers=lms_headers)
    print(lms_response)
    lms_response = json.loads(lms_response.text)
    if lms_response['status'] == 'success':
        Student.objects.filter(id = id).update(is_synced = 1)
        return JsonResponse({'status' : 'success'}, status = 200)
    else:
        return JsonResponse({'status' : 'error'}, status = 200)

@login_required(login_url="login_user")
def studentBulkUpload(request):
    myfile = request.FILES['student_file']
    academic_year = request.POST['academic_year']
    school_class = request.POST['school_class']
    section = request.POST['section']
    category = request.POST['category']
    fs = FileSystemStorage()
    filename = fs.save(myfile.name, myfile)
    uploaded_file_url = fs.url(filename)              
    empexceldata = pd.read_excel(filename)        
    dbframe = empexceldata
    print(dbframe)
    for dbframe in dbframe.itertuples():
        user = User.objects.create(
            username = dbframe.First_name,
            first_name = dbframe.First_name,
            last_name = dbframe.Last_name,
            password = make_password("23wesdxc@#WESDXC%"),
            is_staff = 1,
            is_active = 1,
            is_superuser = 0,
        )

        parent = Parent.objects.create(
            mother_first_name = dbframe.Mother_first_name,
            mother_mobile = dbframe.Mother_mobile,
            mother_email = dbframe.Mother_email,
            father_first_name = dbframe.Father_first_name,
            father_email = dbframe.Father_email,
            father_mobile = dbframe.Father_mobile,
        )
        Student.objects.create(
            admission_no = dbframe.Admission_no,
            roll_no = dbframe.Roll_no,
            academic_year = academic_year,
            gender = dbframe.Gender,
            dob = dbframe.Dob,
            admission_data = dbframe.Admission_data,
            mobile = dbframe.Father_mobile,
            school_class = Class.objects.get(id = school_class),
            creator_id = request.user.id,
            parent_id = parent.id,
            address = dbframe.Address,
            user_id = user.id,
            category = Categories.objects.get(id = category),
            section = Section.objects.get(id = section),
        )
    messages.success(request, 'All Students added successfully')
    return redirect('studentIndex')  

@login_required(login_url='login_user')
def departmentIndex(request):
    departments = Department.objects.filter(creator = request.user.id)
    department_form = forms.AddDepartmentForm()
    if request.method == "POST":
        response_data = {}
        response_data['department_name'] = request.POST.get('department_name')
        Department.objects.create(
            department_name = request.POST.get('department_name'),
            creator = request.user
        )
        messages.success(request, 'Department added successfully.')
    return render(request, app_name+"/departments/index.html", {"departments" : departments, "department_form" : department_form})

@login_required(login_url="login_user")
def departmentDelete(request, id):
    department = Department.objects.get(id = id)
    department.delete()
    messages.success(request, "Department deleted Successfully.")
    return redirect('departmentIndex')

@login_required(login_url='login_user')
def departmentEdit(request, id):
    department = Department.objects.get(id = id)
    department_form = forms.AddDepartmentForm(instance=department)
    form_html = ''
    for form_data in department_form:
        form_html += '<div class="row mb-3"><label class="form-label col-sm-3 col-form-label">' + str(form_data.label) + ':</label><div class="col-sm-9">' + str(form_data) + '</div></div>'
    return JsonResponse({'department_form' : form_html}, status = 200)

@login_required(login_url="login_user")
def departmentUpdate(request):
    if request.method == "POST":
        Department.objects.filter(id = request.POST.get('id')).update(
            department_name = request.POST.get('department_name'),
            is_synced = 0
        )
        messages.success(request, 'Department updated successfully.')
    else:
        messages.error(request, 'Oops, Something went worng')
    return redirect('departmentIndex')

@login_required(login_url='login_user')
def designationIndex(request):
    designations = Designation.objects.filter(creator = request.user.id)
    designation_form = forms.AddDesignationForm()
    if request.method == "POST":
        response_data = {}
        response_data['designation_name'] = request.POST.get('designation_name')
        Designation.objects.create(
            designation_name = request.POST.get('designation_name'),
            creator = request.user
        )
        messages.success(request, 'Designation added successfully.')
    return render(request, app_name+"/designations/index.html", {"designations" : designations, "designation_form" : designation_form})

@login_required(login_url="login_user")
def designationDelete(request, id):
    designation = Designation.objects.get(id = id)
    designation.delete()
    messages.success(request, "Designation deleted Successfully.")
    return redirect('designationIndex')

@login_required(login_url='login_user')
def designationEdit(request, id):
    designation = Designation.objects.get(id = id)
    designation_form = forms.AddDesignationForm(instance=designation)
    form_html = ''
    for form_data in designation_form:
        form_html += '<div class="row mb-3"><label class="form-label col-sm-3 col-form-label">' + str(form_data.label) + ':</label><div class="col-sm-9">' + str(form_data) + '</div></div>'
    return JsonResponse({'designation_form' : form_html}, status = 200)

@login_required(login_url='login_user')
def designationUpdate(request):
    if request.method == "POST":
        Designation.objects.filter(id = request.POST.get('id')).update(
            designation_name = request.POST.get('designation_name'),
            is_synced = 0
        )
        messages.success(request, 'Designation updated successfully.')
    else:
        messages.error(request, 'Oops, Something went worng')
    return redirect('designationIndex')

@login_required(login_url="login_user")
def departmentSync(request, id):
    department = Department.objects.get(id = id)
    ais_url = "https://ais.tabschool.in/api/department-store"
    ais_data = {
        'name' : department.department_name,
        }
    ais_token = SessionManager.objects.get(user_id = request.user.id, productType = 'ais')
    ais_headers={'Content-type': 'application/json', 'Accept': 'text/plain',"Authorization":ais_token.token}
    ais_response = requests.post(ais_url, data=json.dumps(ais_data), headers=ais_headers)
    print(ais_response)
    ais_response = json.loads(ais_response.text)
    
    if ais_response == 200:
        Department.objects.filter(id = id).update(is_synced = 1)
        return JsonResponse({'status' : 'success'}, status = 200)
    else:
        return JsonResponse({'status' : 'error'}, status = 200)

@login_required(login_url='login_user')
def roleIndex(request):
    roles = Role.objects.filter(creator = request.user.id)
    role_form = forms.AddRoleForm()
    if request.method == "POST":
        response_data = {}
        response_data['role_name'] = request.POST.get('role_name')
        Role.objects.create(
            role_name = request.POST.get('role_name'),
            creator = request.user
        )
        messages.success(request, 'Role added successfully.')
    return render(request, app_name+"/roles/index.html", {"roles" : roles, "role_form" : role_form})

@login_required(login_url="login_user")
def roleDelete(request, id):
    role = Role.objects.get(id = id)
    role.delete()
    messages.success(request, "Role deleted Successfully.")
    return redirect('roleIndex')

@login_required(login_url='login_user')
def roleEdit(request, id):
    role = Role.objects.get(id = id)
    role_form = forms.AddRoleForm(instance=role)
    form_html = ''
    for form_data in role_form:
        form_html += '<div class="row mb-3"><label class="form-label col-sm-3 col-form-label">' + str(form_data.label) + ':</label><div class="col-sm-9">' + str(form_data) + '</div></div>'
    return JsonResponse({'role_form' : form_html}, status = 200)

@login_required(login_url='login_user')
def roleUpdate(request):
    if request.method == "POST":
        Role.objects.filter(id = request.POST.get('id')).update(
            role_name = request.POST.get('role_name'),
            is_synced = 0
        )
        messages.success(request, 'Role updated successfully.')
    else:
        messages.error(request, 'Oops, Something went worng')
    return redirect('roleIndex')

@login_required(login_url="login_user")
def teacherIndex(request):
    teacher_form = forms.AddTeacherForm()
    teacher_user_form = forms.AddTeacherUserForm()
    teachers = Teacher.objects.filter(creator = request.user.id)
    bulk_teacher_form = forms.BulkTeachersUploadForm()
    if request.method == 'POST':
        user = User.objects.create(
            username = request.POST.get('first_name')+request.POST.get('last_name'),
            first_name = request.POST.get('first_name'),
            last_name = request.POST.get('last_name'),
            email = request.POST.get('email'),
            password = make_password("23wesdxc@#WESDXC%"),
            is_staff = 1,
            is_active = 1,
            is_superuser = 0,
        )

        Teacher.objects.create(
            staff_no = request.POST.get('staff_no'),
            mobile = request.POST.get('mobile'),
            role = Role.objects.get(id = request.POST.get('role')),
            department = Department.objects.get(id = request.POST.get('department')),
            designation = Designation.objects.get(id = request.POST.get('designation')),
            dob = request.POST.get('dob'),
            qualification = request.POST.get('qualification'),
            address = request.POST.get('address'),
            user_id = user.id,
            creator = request.user
        )
        messages.success(request, 'Teacher added successfully.')
    return render(request, app_name+"/teachers/index.html", {'teacher_form' : teacher_form, 'teacher_user_form' : teacher_user_form, 'teachers' : teachers, 'bulk_teacher_form' : bulk_teacher_form})

@login_required(login_url="login_user")
def teacherDelete(request, id):
    teacher = Teacher.objects.get(id = id)
    User.objects.filter(id = teacher.user.id).delete()
    teacher.delete()
    messages.success(request, "Teacher deleted Successfully.")
    return redirect('teacherIndex')

@login_required(login_url='login_user')
def teacherEdit(request, id):
    teacher = Teacher.objects.get(id = id)
    user = User.objects.get(id = teacher.user.id)
    teacher_form = forms.AddTeacherForm(instance=teacher)
    teacher_user_form = forms.AddTeacherUserForm(instance=user)
    form_html = '<div class="row mb-3"><div class="col-md-3"><label class="form-label" for="staff_no">' + str(teacher_form.fields['staff_no'].label) + '</label>' + str(teacher_form['staff_no']) + '</div><div class="col-md-3"><label class="form-label" for="role">' + str(teacher_form.fields['role'].label) + '</label>' + str(teacher_form['role']) + '</div><div class="col-md-3"><label class="form-label" for="department">' + str(teacher_form.fields['department'].label) + '</label>' + str(teacher_form['department']) + '</div><div class="col-md-3"><label class="form-label" for="designation">' + str(teacher_form.fields['designation'].label) + '</label>' + str(teacher_form['designation']) + '</div></div><div class="row mb-3"><div class="col-md-6"><label class="form-label" for="first_name">' + str(teacher_user_form.fields['first_name'].label) + '</label>' + str(teacher_user_form['first_name']) + '</div><div class="col-md-6"><label class="form-label" for="last_name">' + str(teacher_user_form.fields['last_name'].label) + '</label>' + str(teacher_user_form['last_name']) + '</div></div><div class="row mb-3"><div class="col-md-4"><label class="form-label" for="gender">' + str(teacher_form.fields['gender'].label) + '</label>' + str(teacher_form['gender']) + '</div><div class="col-md-4"><label class="form-label" for="dob">' + str(teacher_form.fields['dob'].label) + '</label>' + str(teacher_form['dob']) + '</div><div class="col-md-4"><label class="form-label" for="qualification">' + str(teacher_form.fields['qualification'].label) + '</label>' + str(teacher_form['qualification']) + '</div></div><div class="row mb-3"><div class="col-md-6"><label class="form-label" for="mobile">' + str(teacher_form.fields['mobile'].label) + '</label>' + str(teacher_form['mobile']) + '</div><div class="col-md-6"><label class="form-label" for="email">' + str(teacher_user_form.fields['email'].label) + '</label>' + str(teacher_user_form['email']) + '</div></div><div class="row mb-3"><div class="col-md-12"><label class="form-label" for="address">' + str(teacher_form.fields['address'].label) + '</label>' + str(teacher_form['address']) + '</div></div>'
    return JsonResponse({'teacher_form' : form_html}, status = 200)

@login_required(login_url="login_user")
def teacherUpdate(request):
    if request.method == "POST":
        teacher = Teacher.objects.get(id = request.POST.get('id'))
        Teacher.objects.filter(id = request.POST.get('id')).update(
            staff_no = request.POST.get('staff_no'),
            mobile = request.POST.get('mobile'),
            role = Role.objects.get(id = request.POST.get('role')),
            department = Department.objects.get(id = request.POST.get('department')),
            designation = Designation.objects.get(id = request.POST.get('designation')),
            dob = request.POST.get('dob'),
            qualification = request.POST.get('qualification'),
            address = request.POST.get('address')
        )

        User.objects.filter(id = teacher.user.id).update(
            username = request.POST.get('first_name')+request.POST.get('last_name'),
            first_name = request.POST.get('first_name'),
            last_name = request.POST.get('last_name'),
            email = request.POST.get('email')
        )
        messages.success(request, 'Teacher updated successfully.')
    else:
        messages.error(request, 'Oops, Something went worng')
    return redirect('teacherIndex')

@login_required(login_url="login_user")
def teacherSync(request, id):
    teacher = Teacher.objects.get(id = id)
    teacher_user = User.objects.get(id = teacher.user.id)
    lms_url = "https://lms.tabschool.in/app/api/add-teacher"
    data = {
        'first_name': teacher_user.first_name,
        'last_name': teacher_user.last_name,
        'gender': teacher.gender,
        'dob': teacher.dob,
        'email': teacher_user.email,
        'mobile': teacher.mobile,
        'address': teacher.qualification ,
        'qualification': teacher.qualification,
        }
    lms_token = SessionManager.objects.get(user_id = request.user.id, productType = 'lms')
    lms_headers = {'Content-type': 'application/json', 'Accept': 'text/plain',"Authorization":"Bearer "+lms_token.token}
    lms_response = requests.post(lms_url, data=json.dumps(data, indent=4, sort_keys=True, default=str), headers=lms_headers)
    lms_response = json.loads(lms_response.text)
    if lms_response['status'] == 'success':
        Teacher.objects.filter(id = id).update(is_synced = 1)
        return JsonResponse({'status' : 'success'}, status = 200)
    else:
        return JsonResponse({'status' : 'error'}, status = 200)

@login_required(login_url='login_user')
def teacherBulkUpload(request):
    myfile = request.FILES['teacher_file']
    role = request.POST['role']
    department = request.POST['department']
    designation = request.POST['designation']
    fs = FileSystemStorage()
    filename = fs.save(myfile.name, myfile)
    uploaded_file_url = fs.url(filename)              
    empexceldata = pd.read_excel(filename)        
    dbframe = empexceldata
    for dbframe in dbframe.itertuples():
        user = User.objects.create(
            username = dbframe.First_name+dbframe.Last_name,
            first_name = dbframe.First_name,
            last_name = dbframe.Last_name,
            email = dbframe.Email,
            password = make_password("23wesdxc@#WESDXC%"),
            is_staff = 1,
            is_active = 1,
            is_superuser = 0,
        )
        Teacher.objects.create(
            staff_no = dbframe.Staff_No,
            mobile = dbframe.Mobile,
            role = Role.objects.get(id = role),
            department = Department.objects.get(id = department),
            designation = Designation.objects.get(id = designation),
            dob = dbframe.Dob,
            qualification = dbframe.Qualification,
            address = dbframe.Address,
            user_id = user.id,
            creator = request.user
        )
    messages.success(request, 'All Teachers added successfully')
    return redirect('teacherIndex')