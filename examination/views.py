from django.shortcuts import render
from .models import Question

# Create your views here.
def exam(request):
    questions=Question.objects.all()
    return render(request,'examination/exam.html',{'questions':questions})