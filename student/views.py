from django.shortcuts import render,HttpResponseRedirect
from .forms import StudentForm,UserForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import Group,User
from examination.models import Course, Question
from django.contrib.auth.decorators import login_required,user_passes_test
from core.views import is_student,is_teacher,is_admin
from examination import models as exam_models
from student import models as stu_models


# Create your views here.
def student_home(request):
    return render(request,'student/studenthome.html')



def student_signup(request):
    if request.method=='POST':
        user_form = UserForm(request.POST)
        student_form = StudentForm(request.POST,request.FILES)
        if user_form.is_valid() and student_form.is_valid():
            user = user_form.save()
            student = student_form.save(commit=False)
            student.user = user
            student.save()
            student_group,created = Group.objects.get_or_create(name='STUDENT')
            user.groups.add(student_group)
            return HttpResponseRedirect('/student/studentlogin/')
    else:
        user_form = UserForm()
        student_form = StudentForm()
    return render(request,'student/studentsignup.html',{'userform':user_form,'studentform':student_form})



def student_login(request):
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
            authform = AuthenticationForm()
        return render(request,'student/studentlogin.html',{'authform':authform})
    else:
        return HttpResponseRedirect('/student/studentdashboard/')



@login_required(login_url='studentlogin')
def student_dashboard(request):
        user=request.user
        if(is_student(user)):
            no_of_exams=exam_models.Course.objects.all().count()
            no_of_questions=exam_models.Question.objects.all().count()
            context={
                'registered_courses':no_of_exams,
                'registered_questions':no_of_questions,
                'student':stu_models.Student.objects.get(user=user)
            }
            return render(request,'student/studentdashboard.html',context=context)



@user_passes_test(is_student)
@login_required(login_url='studentlogin')
def student_logout(request):
        logout(request)
        return HttpResponseRedirect('/student/studentlogin/')



@user_passes_test(is_student)
@login_required(login_url='studentlogin')
def student_dashboard_exam(request):
    courses=exam_models.Course.objects.all()
    return render(request,'student/studentdashboardexam.html',{'registered_courses':courses})



@user_passes_test(is_student)
@login_required(login_url='studentlogin')
def student_dashboard_marks(request):
    courses=exam_models.Course.objects.all()
    return render(request,'student/studentdashboardmarks.html',{'registered_courses':courses})



@user_passes_test(is_student)
@login_required(login_url='studentlogin')
def student_dashboard_instructions(request,pk):
    course=exam_models.Course.objects.get(id=pk)
    return render(request,'student/studentdashboardinstructions.html',{'course':course})



@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_dashboard_exam_start_exam(request,pk):
    course=exam_models.Course.objects.get(id=pk)
    questions=exam_models.Question.objects.filter(course=course)
    if request.method=='POST':
        pass
    response= render(request,'student/studentdashboardexamstartexam.html',{'questions':questions})
    response.set_cookie('course_id',course.id)
    return response



@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_dashboard_exam_calculate_marks(request):
    if request.COOKIES.get('course_id') is not None:
        course_id = request.COOKIES.get('course_id')
        course=exam_models.Course.objects.get(id=course_id)
        total_marks=0
        questions=exam_models.Question.objects.all().filter(course=course)
        for i in range(len(questions)):
            selected_ans = request.COOKIES.get(str(i+1))
            actual_answer = questions[i].answer
            if selected_ans == actual_answer:
                total_marks = total_marks + questions[i].marks
        student = stu_models.Student.objects.get(user_id=request.user.id)
        result = exam_models.Result()
        result.marks=total_marks
        result.exam=course
        result.student=student
        result.save()
        return HttpResponseRedirect('/student/studentdashboardmarks/')


        
@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_dashboard_marks_view_marks(request,pk):
    course=exam_models.Course.objects.get(id=pk)
    student = exam_models.Student.objects.get(user_id=request.user.id)
    results= exam_models.Result.objects.all().filter(exam=course).filter(student=student)
    return render(request,'student/studentdashboardmarksviewmarks.html',{'results':results})


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def update_student(request,pk):
    student=stu_models.Student.objects.get(id=pk)
    user=User.objects.get(id=student.user_id)
    student_form=StudentForm(instance=student)
    user_form=UserForm(instance=user)
    if request.method=='POST':
        user_form=UserForm(request.POST,instance=user)
        student_form=StudentForm(request.POST,request.FILES,instance=student)
        if user_form.is_valid() and student_form.is_valid():
            user=user_form.save()
            student=student_form.save(commit=False)
            student.user=user
            student.save()
            return HttpResponseRedirect('/student/studentdashboard/')
    context={
        'userform':user_form,
        'studentform':student_form,
    }

    return render(request,'student/updatestudent.html',context=context)
