from django.urls import path
from . import views

urlpatterns = [
    path('studenthome/',views.student_home,name='studenthome'),
    path('studentsignup/',views.student_signup,name='studentsignup'),
    path('studentlogin/',views.student_login,name='studentlogin'),
    path('studentdashboard/',views.student_dashboard,name='studentdashboard'),
    path('studentlogout/',views.student_logout,name='studentlogout'),
    path('studentdashboardexam/',views.student_dashboard_exam,name='studentdashboardexam'),
    path('studentdashboardmarks/',views.student_dashboard_marks,name='studentdashboardmarks'),
    path('studentdashboardinstructions/<int:pk>/',views.student_dashboard_instructions,name='studentdashboardinstructions'),
    path('studentdashboardexamstartexam/<int:pk>/',views.student_dashboard_exam_start_exam,name='studentdashboardexamstartexam'),
    path('studentdashboardexamcalculatemarks/',views.student_dashboard_exam_calculate_marks,name='studentdashboardexamcalculatemarks'),
    path('studentdashboardmarksviewmarks/<int:pk>/',views.student_dashboard_marks_view_marks,name='studentdashboardmarksviewmarks'),
    path('updatestudent/<int:pk>/',views.update_student,name='updatestudent'),
]
