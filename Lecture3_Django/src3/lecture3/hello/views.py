from django.http import HttpResponse
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "hello/index.html")

def xana(request):
    return HttpResponse("Hello, Xana!")

def facu(request):
    return HttpResponse("Hello, Facu!")

def greet(request, name):
    return render(request, "hello/greet.html",{
        "name": name.capitalize()
    })