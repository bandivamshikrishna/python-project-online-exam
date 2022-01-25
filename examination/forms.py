from django import forms
from .models import Course,Question

class CourseForm(forms.ModelForm):
    class Meta:
        model=Course
        fields=['course_name','no_of_questions','total_marks']



class QuestionForm(forms.ModelForm):
    courseid=forms.ModelChoiceField(queryset=Course.objects.all(), to_field_name="id")
    class Meta:
        model=Question
        fields=['marks','question','option1','option2','option3','option4','answer']