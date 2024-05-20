from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
# Create your views here.
from django.core.files.storage import FileSystemStorage
from .models import PersonnelItem
from django.core.paginator import Paginator
from .forms import UploadFileForm
import openpyxl
from .forms import searchPersonnel

def search_Personnel(request):
    form = searchPersonnel()
    query = None
    results = []
    if 'Name' in request.GET:
        form = searchPersonnel(request.GET)
        if form.is_valid():
            query = form.cleaned_data['Name']
            results = PersonnelItem.objects.filter(title__icontains=query)
    return render(request, 'myapp/index.html', {'form': form, 'query': query, 'results': results})



def UploadFile(request):
    # Logic to handle personnel records
    return render(request, 'myapp/upload.html')
    

def custom_404(request, exception):
    return render(request, 'other/404.html', status=404)


def index(request):
    if request.method == 'GET':
        form = UploadFileForm(request.GET, request.FILES)
        persons = PersonnelItem.objects.all()
        paginator = Paginator(persons,5)
        page_num = request.GET.get("page")
        persons = paginator.get_page(page_num)
        return render(request, 'myapp/index.html', {'persons': persons})
    # return render(request,"myapp/testSidebar.html",{})



def Personnel_Records(request):
    if request.method == 'GET':
            form = UploadFileForm(request.GET, request.FILES)
    persons = PersonnelItem.objects.all()
    paginator = Paginator(persons,5)
    page_num = request.GET.get("page")
    persons = paginator.get_page(page_num)
    return render(request, 'Base/sidebar.html', {'persons': persons})
    # return render(request,"myapp/testSidebar.html",{})


def placementOfficer(request):
    return render(request,"myapp/placementOfficer.html",{})

def inactivepersonnel(request):
    return render(request,"myapp/InactivePersonnel.html",{})



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
            return redirect('myapp/index.html')
    else:
        form = UploadFileForm()
    return render(request, 'myapp/index.html', {'form': form})

def display_data(request):
    persons = PersonnelItem.objects.all()
    paginator = Paginator(persons,5)
    page_num = request.GET.get("page")
    persons = paginator.get_page(page_num)
    return render(request, 'myapp/01base.html', {'persons': persons})




def edit_item(request, item_id):
    def edit_item(request, item_id):
        item = get_object_or_404(PersonnelItem, id=item_id)
        if request.method == 'POST':
            form = ItemForm(request.POST, instance=item)
            if form.is_valid():
                form.save()
                return redirect('item_list')
        else:
            form = ItemForm(instance=item)
        return render(request, 'edit_item.html', {'form': form, 'item': item})