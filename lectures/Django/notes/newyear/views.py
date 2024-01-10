from django.shortcuts import render
from datetime import datetime


# Create your views here.
def index(request):
    now = datetime.now()
    return render(request, "newyear/index.html", {
        "newyear": now.day == 9 and now.month == 1 
    })
