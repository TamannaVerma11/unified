from django import forms
from .models import *

GENDER= (
('Male', 'M'),
('Feamle', 'F'),
)

class BaseForm(forms.ModelForm):
    pass

class LoginForm(BaseForm):
    class Meta:
        model = Login
        fields = ['email', 'password']
        widgets = {
            'email' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Enter Email'}),
            'password' : forms.PasswordInput(attrs={'class' : 'form-control', 'placeholder' : 'Enter Password'})
        }

class AddClassForm(BaseForm):
    class Meta:
        model = Class
        fields = ['class_name', 'medium']
        widgets = {
            'class_name' : forms.TextInput(attrs={'class' : 'form-control mb-3', 'placeholder' : 'Enter Class'}),
            'medium' : forms.Select(attrs={'class' : 'form-control mb-3', 'placeholder' : 'Enter Class'}),
        }

class AddSectionForm(BaseForm):
    class Meta:
        model = Section
        fields = ['section_name']
        widgets = {
            'section_name' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Enter Section Name'})
        }

class AddCategoryForm(BaseForm):
    class Meta:
        model = Categories
        fields = ['category_name']
        widgets = {
            'category_name' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Enter Category Name'})
        }

class AddMediumForm(BaseForm):
    class Meta:
        model = Medium
        fields = ['medium_name']
        widgets = {
            'medium_name' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Enter Medium'})
        }

class AddStudentForm(BaseForm):
    gender = forms.ChoiceField(choices=GENDER, widget=forms.Select(attrs={'class' : 'form-control'}))
    class Meta:
        model = Student
        fields = ['admission_no', 'roll_no', 'school_class', 'section', 'academic_year', 'gender', 'dob', 'admission_data', 'address', 'mobile', 'category']
        widgets = {
            'admission_no' : forms.TextInput(attrs={'class' : 'form-control'}), 
            'roll_no' : forms.TextInput(attrs={'class' : 'form-control'}), 
            'school_class' : forms.Select(attrs={'class' : 'form-control mb-3'}), 
            'section' : forms.Select(attrs={'class' : 'form-control mb-3'}), 
            'academic_year' : forms.TextInput(attrs={'class' : 'form-control'}), 
            'dob' : forms.DateInput(format=('%d/%m/%Y'), attrs={'class': 'form-control', 'placeholder': 'Select a date', 'type': 'date'}), 
            'admission_data' : forms.DateInput(format=('%d/%m/%Y'), attrs={'class': 'form-control', 'placeholder': 'Select a date', 'type': 'date'}), 
            'address' : forms.TextInput(attrs={'class' : 'form-control'}), 
            'mobile' : forms.TextInput(attrs={'class' : 'form-control'}), 
            'category' : forms.Select(attrs={'class' : 'form-control mb-3'}),
        }

class AddParentForm(BaseForm):
    class Meta:
        model = Parent
        fields = ['mother_first_name', 'mother_last_name', 'mother_mobile', 'mother_email', 'father_first_name', 'father_last_name', 'father_mobile', 'father_email']
        widgets = {
            'mother_first_name' : forms.TextInput(attrs={'class' : 'form-control'}),
            'mother_last_name' : forms.TextInput(attrs={'class' : 'form-control'}),
            'mother_mobile' : forms.TextInput(attrs={'class' : 'form-control'}),
            'mother_email' : forms.TextInput(attrs={'class' : 'form-control'}),
            'father_first_name' : forms.TextInput(attrs={'class' : 'form-control'}),
            'father_last_name' : forms.TextInput(attrs={'class' : 'form-control'}),
            'father_mobile' : forms.TextInput(attrs={'class' : 'form-control'}),
            'father_email' : forms.TextInput(attrs={'class' : 'form-control'}),
        }

class AddStudentUserForm(BaseForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
        widgets = {
            'first_name' : forms.TextInput(attrs={'class' : 'form-control'}),
            'last_name' : forms.TextInput(attrs={'class' : 'form-control'}),
        }
    
class AddDepartmentForm(BaseForm):
    class Meta:
        model = Department
        fields = ['department_name']
        widgets = {
            'department_name' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Enter Department Name'})
        }

class AddDesignationForm(BaseForm):
    class Meta:
        model = Designation
        fields = ['designation_name']
        widgets = {
            'designation_name' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Enter Designation Name'})
        }

class AddRoleForm(BaseForm):
    class Meta:
        model = Role
        fields = ['role_name']
        widgets = {
            'role_name' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Enter Role Name'})
        }

class AddTeacherForm(BaseForm):
    gender = forms.ChoiceField(choices=GENDER, widget=forms.Select(attrs={'class' : 'form-control'}))
    class Meta:
        model = Teacher
        fields = ['staff_no', 'role', 'department', 'designation', 'gender', 'dob', 'qualification', 'address', 'mobile']
        widgets = {
            'staff_no' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Enter Staff  Number'}), 
            'mobile' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Enter Mobile  Number'}), 
            'role' : forms.Select(attrs={'class' : 'form-control mb-3'}),  
            'department' : forms.Select(attrs={'class' : 'form-control mb-3'}),  
            'designation' : forms.Select(attrs={'class' : 'form-control mb-3'}), 
            'dob' : forms.DateInput(format=('%d/%m/%Y'), attrs={'class': 'form-control', 'placeholder': 'Select a date', 'type': 'date'}), 
            'qualification' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Enter Qualification'}), 
            'address' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Enter Address'}), 
        }

class AddTeacherUserForm(BaseForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name' : forms.TextInput(attrs={'class' : 'form-control'}),
            'last_name' : forms.TextInput(attrs={'class' : 'form-control'}),
            'email' : forms.TextInput(attrs={'class' : 'form-control'}),
        }
