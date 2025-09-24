from django.shortcuts import render

# Create your views here.

def homeView(request):
    students = {'name':'Akshay'}
    return render(request,'base.html',students)
