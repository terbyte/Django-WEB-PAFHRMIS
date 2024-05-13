from django.shortcuts import render
from django.http import HttpResponse
from .models import Placement,Personnel_Item
# Create your views here.


def index(response,id):
    ls =Personnel_Item.objects.get(id =id)
    return render (response,"myapp/placement.html",{"FULLNAME":ls.FULLNAME})

def Personnel_Records(response):
    return render(response,"myapp/Personnel_Records.html",{})

def Placement(response):
    return render(response,"myapp/placement.html",{})

