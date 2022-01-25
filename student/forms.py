from typing import Tuple
from django.contrib.auth.models import User
from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.forms.fields import CharField
from .models import Student

class UserForm(UserCreationForm):
    first_name=CharField(required=True,error_messages={'required':'enter your first name'})
    last_name=CharField(required=True,error_messages={'required':'enter your last name'})
    email=CharField(required=True,error_messages={'required':'enter your email name'})
    class Meta:
        model=User
        fields=['username','first_name','last_name','email']
        error_messages={'username':{'required':'enter your username'},
        }

class StudentForm(forms.ModelForm):
    class Meta:
        model=Student
        fields=['address','contact','profile_pic']
