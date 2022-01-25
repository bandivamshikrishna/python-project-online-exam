from django.urls import path
from . import views 

urlpatterns = [
    path('teacherhome/',views.teacher_home,name='teacherhome'),
    path('teachersignup/',views.teacher_signup,name='teachersigup'),
    path('teacherlogin/',views.teacher_login,name='teacherlogin'),
    path('teacherdashboard/',views.teacher_dashboard,name='teacherdashboard'),
    path('teacherlogout/',views.teacher_logout,name='teacherlogout'),
    path('teacherdashboardcourse/',views.teacher_dashboard_course,name='teacherdashboardcourse'),
    path('teacherdashboardquestion/',views.teacher_dashboard_question,name='teacherdashboardquestion'),
    path('teacherdashboardcourseaddcourse/',views.teacher_dashboard_course_add_course,name='teacherdashboardcourseaddcourse'),
    path('teacherwaitforapproval/',views.teacher_wait_for_approval,name='teacherwaitforapproval'),
    path('teacherdashboardcourseviewcourse/',views.teacher_dashboard_course_view_course,name='teacherdashboardcourseviewcourse'),
    path('teacherdashboarddeletecourse/<int:pk>/',views.teacher_dashboard_delete_course,name='teacherdashboarddeletecourse'),
    path('teacherdashboardquestionaddquestion/',views.teacher_dashboard_question_add_question,name='teacherdashboardquestionaddquestion'),
    path('teacherdashboardquestionviewquestion/',views.teacher_dashboard_question_view_question,name='teacherdashboardquestionviewquestion'),
    path('teacherdashboardsubjectquestions/<int:pk>/',views.teacher_dashboard_subject_questions,name='teacherdashboardsubjectquestions'),
    path('teacherdashboarddeletesubjectquestions/<int:pk>/',views.teacher_dashboard_delete_subject_question,name='teacherdashboarddeletesubjectquestion'),
    path('updateteacher/<int:pk>/',views.update_teacher,name='updateteacher'),
]
