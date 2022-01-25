from django.shortcuts import render,HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserForm,TeacherForm
from django.contrib.auth.models import Group,User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from core.views import is_student,is_teacher,is_admin
from student import models as stu_models 
from examination import models as exam_models
from examination import forms as exam_forms
from django.contrib.auth.decorators import login_required,user_passes_test
from . import models as tea_models



# Create your views here.
def teacher_home(request):
    return render(request,'teacher/teacherhome.html')

def teacher_signup(request):
    if request.method=='POST':
        user_form=UserForm(request.POST)
        teacher_form=TeacherForm(request.POST,request.FILES)
        if user_form.is_valid() and teacher_form.is_valid():
            user=user_form.save()
            teacher=teacher_form.save(commit=False)
            teacher.user=user
            teacher.save()
            teacher_group,created=Group.objects.get_or_create(name='TEACHER')
            user.groups.add(teacher_group)
            return HttpResponseRedirect('/teacher/teacherlogin/')
    else:
        user_form=UserForm()
        teacher_form=TeacherForm()
    return render(request,'teacher/teachersignup.html',{'userform':user_form,'teacherform':teacher_form})


def teacher_login(request):
    if not request.user.is_authenticated:
        if request.method=='POST':
            authform=AuthenticationForm(request=request,data=request.POST)
            if authform.is_valid():
                uname=authform.cleaned_data['username']
                upass=authform.cleaned_data['password']
                user=authenticate(username=uname,password=upass)
                if user is not None:
                    login(request,user)
                    return HttpResponseRedirect('/accountlogin/')
        else:
            authform=AuthenticationForm()
        return render(request,'teacher/teacherlogin.html',{'authform':authform})
    else:
        return HttpResponseRedirect('/teacher/teacherdashboard/')

@login_required(login_url='teacherlogin')
def teacher_dashboard(request):
    user=request.user
    if(is_teacher(user)):
        no_of_students=stu_models.Student.objects.all().count() 
        no_of_courses=exam_models.Course.objects.all().count()
        no_of_questions=exam_models.Question.objects.all().count()
        context={
            'registered_students':no_of_students,
            'registered_courses':no_of_courses,
            'registered_questions':no_of_questions,

        }
        return render(request,'teacher/teacherdashboard.html',context=context)
    

@login_required(login_url='teacherlogin')
def teacher_logout(request):
    logout(request)
    return HttpResponseRedirect('/teacher/teacherlogin/')


@login_required(login_url='teacherlogin')
def teacher_dashboard_course(request):
    return render(request,'teacher/teacherdashboardcourse.html')


@login_required(login_url='teacherlogin')
def teacher_dashboard_question(request):
    return render(request,'teacher/teacherdashboardquestion.html')


def teacher_wait_for_approval(request):
    return render(request,'teacher/teacherwaitforapproval.html')

@login_required(login_url='teacherlogin')
def teacher_dashboard_course_add_course(request):
    if request.method=='POST':
        courseform=exam_forms.CourseForm(request.POST)
        if courseform.is_valid():
            courseform.save()
            courseform=exam_forms.CourseForm()
            messages.success(request,'Course add successfully!!')
    else:
        courseform=exam_forms.CourseForm()
    return render(request,'teacher/teacherdashboardcourseaddcourse.html',{'courseform':courseform})


@user_passes_test(is_teacher)
@login_required(login_url='teacherlogin')
def teacher_dashboard_course_view_course(request):
    courses=exam_models.Course.objects.all()
    context={
        'registered_courses':courses
    }
    return render(request,'teacher/teacherdashboardcourseviewcourse.html',context=context)


@user_passes_test(is_teacher)
@login_required(login_url='teacherlogin')
def teacher_dashboard_delete_course(request,pk):
    course=exam_models.Course.objects.get(id=pk)
    course.delete()
    messages.success(request,'Course deleted Successfully!!') 
    return HttpResponseRedirect('/teacher/teacherdashboardcourseviewcourse/')



@user_passes_test(is_teacher)
@login_required(login_url='teacherlogin')
def teacher_dashboard_question_add_question(request):
    if request.method=='POST':
        questionform=exam_forms.QuestionForm(request.POST)
        if questionform.is_valid():
            question=questionform.save(commit=False)
            course=exam_models.Course.objects.get(id=request.POST.get('courseid'))
            question.course=course
            question.save() 
            messages.success(request,'Question Added Successfully!!')
            questionform=exam_forms.QuestionForm()
    else:
        questionform=exam_forms.QuestionForm()
    return render(request,'teacher/teacherdashboardquestionaddquestion.html',{'questionform':questionform})


@user_passes_test(is_teacher)
@login_required(login_url='teacherlogin')
def teacher_dashboard_question_view_question(request):
    courses=exam_models.Course.objects.all() 
    context={
        'registered_courses':courses,
    }
    return render(request,'teacher/teacherdashboardquestionviewquestion.html',context=context)


@user_passes_test(is_teacher)
@login_required(login_url='teacherlogin')
def teacher_dashboard_subject_questions(request,pk):
    course=exam_models.Course.objects.get(id=pk)
    questions=exam_models.Question.objects.filter(course=course)
    context={
        'registered_questions':questions,
    }
    return render(request,'teacher/teacherdashboardsubjectquestions.html',context=context)


@user_passes_test(is_teacher)
@login_required(login_url='teacherlogin')
def teacher_dashboard_delete_subject_question(request,pk):
    question=exam_models.Question.objects.get(id=pk)
    question.delete()
    return HttpResponseRedirect('/teacher/teacherdashboardquestionviewquestion/')


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def update_teacher(request,pk):
    teacher=tea_models.Teacher.objects.get(id=pk)
    user=User.objects.get(id=teacher.user_id)
    teacher_form=TeacherForm(instance=teacher)
    user_form=UserForm(instance=user)
    if request.method=='POST':
        teacher_form=TeacherForm(request.POST,request.FILES,instance=teacher)
        user_form=UserForm(request.POST,instance=user)
        if teacher_form.is_valid() and user_form.is_valid():
            user=user_form.save()
            teacher=teacher_form.save(commit=False)
            teacher.user=user
            teacher.save()
            return HttpResponseRedirect('/teacher/teacherdashboard/')

    context={
        'teacherform':teacher_form,
        'userform':user_form,
    }
    return render(request,'teacher/updateteacher.html',context=context)