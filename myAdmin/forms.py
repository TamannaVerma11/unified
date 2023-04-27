from django import forms
from .models import *

class BaseForm(forms.ModelForm):
    pass

class LoginForm(BaseForm):
    class Meta:
        model = Login
        fields = ['username', 'password']
        widgets = {
            'username' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Enter Number'}),
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

class AddMediumForm(BaseForm):
    class Meta:
        model = Medium
        fields = ['medium_name']
        widgets = {
            'medium_name' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Enter Medium'})
        }

    

