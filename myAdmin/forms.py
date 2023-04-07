from django import forms
from .models import *

FRUIT_CHOICES= [
    ('orange', 'Oranges'),
    ('cantaloupe', 'Cantaloupes'),
    ('mango', 'Mangoes'),
    ('honeydew', 'Honeydews'),
    ]

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
        fields = ['class_name', 'section_id']
        widgets = {
            'class_name' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Enter Number'}),
            'section_id' : forms.Select(attrs={'class' : 'form-control'}, choices=FRUIT_CHOICES)
        }

class AddSectionForm(BaseForm):
    class Meta:
        model = Section
        fields = ['section_name']
        widgets = {
            'section_name' : forms.TimeInput(attrs={'class' : 'form-control', 'placeholder' : 'Enter Section Name'})
        }

    

