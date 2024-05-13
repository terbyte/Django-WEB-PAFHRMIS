from django.shortcuts import render,HttpResponse

# Create your views here.


def index(response,id):
    return HttpResponse("<h1>%s</h1>" %id)

def Personnel_Records(request):
    return render(request,"base.html")

def Placement(request):
    return render(request,"placement.html")

