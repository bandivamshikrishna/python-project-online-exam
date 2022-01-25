from django.contrib import admin
from .models import Course,Question,Result

# Register your models here.
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display=['id','course_name','no_of_questions','total_marks']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display=['id','course','question','option1','option2','option3','option4','answer','marks']


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display=['id','student','exam','marks','date']

