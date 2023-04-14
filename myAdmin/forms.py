from django import forms
from .models import *
from django.forms import inlineformset_factory

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
        fields = ['class_name']
        widgets = {
            'class_name' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Enter Number'}),
        }

class AddSectionForm(BaseForm):
    class Meta:
        model = Section
        fields = ['section_name']
        widgets = {
            'section_name' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Enter Section Name'})
        }


    

