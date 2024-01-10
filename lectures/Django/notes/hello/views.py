from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "hello/index.html")

def filip(request):
    return HttpResponse("Hello Filip!!!")

def greet(request, names):
    return render(request, "hello/greet.html", {
        "name": names.capitalize()
    })
