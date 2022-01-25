from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm
from teacher import models as tea_models 
from student import models as stu_models

# Create your views here.
def student_sign_home(request):
    return render(request,'core/studentsignhome.html')



def is_student(user):
    return user.groups.filter(name='STUDENT').exists()

def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()

def is_admin(user):
    if user.is_superuser==True:
        return True
    else:
        return False

def account_login(request):
    if is_student(request.user):      
        return redirect('/student/studentdashboard/')
                
    elif is_teacher(request.user):
        accountapproval=tea_models.Teacher.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('/teacher/teacherdashboard/')
        else:
            return redirect('/teacher/teacherwaitforapproval/')
    else:
        return redirect('/admin/admindashboard/')
