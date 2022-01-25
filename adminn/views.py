from django.shortcuts import render,HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login,logout
from core.views import is_admin, is_student,is_teacher,is_admin
from django.contrib.auth.decorators import login_required,user_passes_test
from student import models as stud_models
from teacher import models as tea_models
from examination import models as exam_models
from examination import forms as exam_forms
from django.contrib import messages
from teacher import forms as tea_forms
from django.db.models import Sum
from django.contrib.auth.models import User


# Create your views here.
def admin_login(request):
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
        return render(request,'admin/adminlogin.html',{'authform':authform})
    else:
        return HttpResponseRedirect('/admin/admindashboard/')

@login_required(login_url='adminlogin')
def admin_dashboard(request):
    user=request.user
    if(is_admin(user)):
        no_of_students=stud_models.Student.objects.all().count()
        no_of_teachers=tea_models.Teacher.objects.all().count()
        no_of_courses=exam_models.Course.objects.all().count()
        no_of_questions=exam_models.Question.objects.all().count()
        context={'registered_students':no_of_students,
                 'registered_teachers':no_of_teachers,
                 'registered_courses':no_of_courses,
                 'registered_questions':no_of_questions,
        }
        return render(request,'admin/admindashboard.html',context=context)


@login_required(login_url='adminlogin')
def admin_logout(request):
    logout(request)
    return HttpResponseRedirect('/admin/adminlogin/')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_dashboard_teacher_section(request):
    pending_teachers=tea_models.Teacher.objects.all().filter(status=False).count()
    approved_teachers=tea_models.Teacher.objects.all().filter(status=True).count()
    teachers_salary=tea_models.Teacher.objects.all().filter(status=True).aggregate(Sum('salary'))['salary__sum'],
    context={
        'pending_teachers':pending_teachers,
        'approved_teachers':approved_teachers,
        'teachers_salary':teachers_salary,
    }
    return render(request,'admin/admindashboardteachersection.html',context=context)

@user_passes_test(is_admin)
@login_required(login_url='adminlogin')
def admin_dashboard_student_section(request):
    no_of_students=stud_models.Student.objects.all().count()
    context={
        'registered_students':no_of_students,
    }
    return render(request,'admin/admindashboardstudentsection.html',context=context)


@user_passes_test(is_admin)
@login_required(login_url='adminlogin')
def admin_dashboard_course(request):
    return render(request,'admin/admindashboardcourse.html')


@user_passes_test(is_admin)
@login_required(login_url='adminlogin')
def admin_dashboard_course_add_course(request):
    if request.method=='POST':
        courseform=exam_forms.CourseForm(request.POST)
        if courseform.is_valid():
            courseform.save()
            courseform=exam_forms.CourseForm()
            messages.success(request,'Course add successfully!!')
    else:
        courseform=exam_forms.CourseForm()
    return render(request,'admin/admindashboardcourseaddcourse.html',{'courseform':courseform})

@user_passes_test(is_admin)
@login_required(login_url='adminlogin')
def admin_dashboard_course_view_course(request):
    courses=exam_models.Course.objects.all()
    context={
        'registered_courses':courses
    }
    return render(request,'admin/admindashboardcourseviewcourse.html',context=context)

@user_passes_test(is_admin)
@login_required(login_url='adminlogin')
def admin_dashboard_delete_course(request,pk):
    course=exam_models.Course.objects.get(id=pk)
    course.delete()
    messages.success(request,'Course deleted Successfully!!') 
    return HttpResponseRedirect('/admin/admindashboardcourseviewcourse/')


@user_passes_test(is_admin)
@login_required(login_url='adminlogin')
def admin_dashboard_question(request):
    return render(request,'admin/admindashboardquestion.html')



@user_passes_test(is_admin)
@login_required(login_url='adminlogin')
def admin_dashboard_question_add_question(request):
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
    return render(request,'admin/admindashboardquestionaddquestion.html',{'questionform':questionform})


@user_passes_test(is_admin)
@login_required(login_url='adminlogin')
def admin_dashboard_question_view_question(request):
    courses=exam_models.Course.objects.all() 
    context={
        'registered_courses':courses,
    }
    return render(request,'admin/admindashboardquestionviewquestion.html',context=context)


@user_passes_test(is_admin)
@login_required(login_url='adminlogin')
def admin_dashboard_subject_questions(request,pk):
    course=exam_models.Course.objects.get(id=pk)
    questions=exam_models.Question.objects.filter(course=course)
    context={
        'registered_questions':questions,
    }
    return render(request,'admin/admindashboardsubjectquestions.html',context=context)


@user_passes_test(is_admin)
@login_required(login_url='adminlogin')
def admin_dashboard_delete_subject_question(request,pk):
    question=exam_models.Question.objects.get(id=pk)
    question.delete()
    return HttpResponseRedirect('/admin/admindashboardquestionviewquestion/')


@user_passes_test(is_admin)
@login_required(login_url='adminlogin')
def admin_dashboard_teacher_salary(request):
    teachers=tea_models.Teacher.objects.all().filter(status=True)
    return render(request,'admin/admindashboardteachersalary.html',{'teachers':teachers})


@user_passes_test(is_admin)
@login_required(login_url='adminlogin')
def admin_dashboard_student_registered(request):
    students=stud_models.Student.objects.all()
    return render(request,'admin/admindashboardstudentregistered.html',{'students':students})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_dashboard_student_view_marks(request):
    registered_students=stud_models.Student.objects.all()
    return render(request,'admin/admindashboardstudentviewmarks.html',{'registered_students':registered_students})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_dashboard_student_course_marks(request,pk):
    student=stud_models.Student.objects.get(id=pk)
    registered_courses=exam_models.Course.objects.all()
    context={
        'student':student,
        'registered_courses':registered_courses,
    }
    return render(request,'admin/admindashboardstudentcoursemarks.html',context=context)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_dashboard_student_course_view_marks(request,stuid,corid):
    course=exam_models.Course.objects.get(id=corid)
    student=stud_models.Student.objects.get(id=stuid)
    results=exam_models.Result.objects.all().filter(exam=course).filter(student=student)
    context={
        'course':course,
        'results':results,
        'student':student,
    }
    return render(request,'admin/admindashboardstudentcourseviewmarks.html',context=context)


@user_passes_test(is_admin)
@login_required(login_url='adminlogin')
def admin_dashboard_teachers_approved(request):
    approved_teachers=tea_models.Teacher.objects.all().filter(status=True)
    return render(request,'admin/admindashboardteachersapproved.html',{'approved_teachers':approved_teachers})


@user_passes_test(is_admin)
@login_required(login_url='adminlogin')
def admin_dashboard_teachers_pending(request):
    pending_teachers=tea_models.Teacher.objects.filter(status=False)
    return render(request,'admin/admindashboardteacherspending.html',{'pending_teachers':pending_teachers})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_dashboard_approve_teacher(request,pk):
    if request.method=='POST':
        teachersalaryform=tea_forms.TeacherSalaryForm(request.POST)
        if teachersalaryform.is_valid():
            salary=teachersalaryform.cleaned_data['salary']
            teacher=tea_models.Teacher.objects.get(id=pk)
            teacher.salary=salary
            teacher.status=True
            teacher.save()
            return HttpResponseRedirect('/admin/admindashboard/')
    else:
        teachersalaryform=tea_forms.TeacherSalaryForm()
    return render(request,'admin/admindashboardtsalaryform.html',{'teachersalaryform':teachersalaryform})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_dashboard_reject_teacher(request,pk):
    teacher=tea_models.Teacher.objects.get(id=pk)
    user=User.objects.get(id=teacher.user_id)
    user.delete()
    teacher.delete()
    return HttpResponseRedirect('/admin/admindashboardteacherspending/')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_dashboard_delete_approved_teacher(request,pk):
    teacher=tea_models.Teacher.objects.get(id=pk)
    user=User.objects.get(id=teacher.user_id)
    user.delete()
    teacher.delete()
    return HttpResponseRedirect('/admin/admindashboardteachersapproved/')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_dashboard_delete_registered_students(request,pk):
    student=stud_models.Student.objects.get(id=pk)
    user=User.objects.get(id=student.user_id)
    user.delete()
    student.delete()
    return HttpResponseRedirect('/admin/admindashboardstudentregistered/')
