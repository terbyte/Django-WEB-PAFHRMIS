from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.
from django.core.files.storage import FileSystemStorage
from .models import PersonnelItem
from django.core.paginator import Paginator
from .forms import UploadFileForm
import openpyxl
from datetime import datetime


def index(request,id):
    return render (request,"myapp/01base.html",{"name":"name"})

def Personnel_Records(request):
    return render(request,"myapp/Personnel_Records.html",{"name":"PERSONNEL RECORDS"})

def Placement(request):
    return render(request,"myapp/placement.html",{})

def side(request):
    return render(request,"myapp/testSidebar.html",{})


def display_file_data(request):
    if request.method == 'GET':
        form = UploadFileForm(request.GET, request.FILES)
        





def upload_file(request):

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            file_path = fs.path(filename)
            wb = openpyxl.load_workbook(file_path)
            ws = wb.active
            for row in ws.iter_rows(min_row=30, values_only=True):  
                PersonnelItem.objects.create(
                NR=row[0],
                RANK=row[1],
                LAST_NAME=row[2],
                FIRST_NAME=row[3],
                MIDDLE_NAME=row[4],
                EXTENSION_NAME=row[5],
                SERIAL_NUMBER=row[6],
                BOS=row[7],
                SEX=row[8],
                BIRTHDAY=row[9],
                CONTACT_NUMBER=row[10],
                ADDRESS=row[11],
                REGULAR_RESERVE=row[12],
                PILOT_RATED_NON_RATED=row[13],
                AFSC=row[14],
                HIGHEST_PME_COURSES=row[15],
                EFFECTIVE_DATE_APPOINTMENT=row[16],
                EFFECTIVE_DATE_ENTERED=row[17],
                LENGTH_OF_SERVICE=row[18],
                DATE_LAST_PROMOTION_APPOINTMENT=row[19],
                UNIT=row[20],
                SUB_UNIT=row[21],
                DATE_LAST_1ST_TRANCH_REENLISTMENT=row[22],
                DATE_LAST_2ND_TRANCH_REENLISTMENT=row[23]
                )
            return redirect('display_data')
    else:
        form = UploadFileForm()
    return render(request, 'myapp/01base.html', {'form': form})

def display_data(request):
    persons = PersonnelItem.objects.all()
    paginator = Paginator(persons,5)
    page_num = request.GET.get("page")
    persons = paginator.get_page(page_num)
    return render(request, 'myapp/01base.html', {'persons': persons})

