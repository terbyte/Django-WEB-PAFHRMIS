from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from .forms import UploadFileForm
import openpyxl
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import PersonnelItem


def Tranche(request):
    return render(request, 'reenlistment/Tranche.html')
 


@csrf_exempt  # Only if you don't have CSRF token in the form
def update_personnel(request):
    if request.method == 'POST':
        try:
            personnel_id = request.POST.get('personnel_id')
            personnel_items = PersonnelItem.objects.filter(SERIAL_NUMBER=personnel_id)
            if not personnel_items.exists():
                return JsonResponse({'success': False, 'error': 'Personnel not found'})
            
            personnel_items.update(
                # LAST_NAME=request.POST.get('last_name'),
                # FIRST_NAME=request.POST.get('first_name'),
                # MIDDLE_NAME=request.POST.get('middle_name'),
                ADDRESS=request.POST.get('address'),
                # CATEGORY=request.POST.get('address'),
                RANK=request.POST.get('rank'),
                AFSC=request.POST.get('afsc'),
                UNIT=request.POST.get('unit'),
                SUB_UNIT=request.POST.get('subunit'),
                CONTACT_NUMBER=request.POST.get('contactnum'),
                HIGHEST_PME_COURSES=request.POST.get('hpme'),
                # DATE_LAST_PROMOTION_APPOINTMENT=request.POST.get('promotion'),
                

                # Update other fields similarly
            )
            
            
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request'})


def UploadFile(request):
    # Logic to handle personnel records
    return render(request, 'myapp/upload.html')
    

def custom_404(request, exception):
    return render(request, 'other/404.html', status=404)


# def index(request):
#     if request.method == 'GET':
#         form = UploadFileForm(request.GET, request.FILES)
#         persons = PersonnelItem.objects.all()
#         paginator = Paginator(persons,10)
#         page_num = request.GET.get("page")
#         persons = paginator.get_page(page_num)
#         return render(request, 'myapp/index.html', {'persons': persons})
#     # return render(request,"myapp/testSidebar.html",{})


def placementOfficer(request):
    return render(request,"myapp/placementOfficer.html",{})

def placementEnlisted(request):
    return render(request,"myapp/placementEnlisted.html",{})

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



def index(request):
    last_name_query = request.GET.get('last_name')
    first_name_query = request.GET.get('first_name')
    middle_name_query = request.GET.get('middle_name')
    suffix_query = request.GET.get('suffix')
    afsn_query = request.GET.get('afsn')
    rank_query = request.GET.get('rank')
    classification_query = request.GET.get('classification')
    sex_query = request.GET.get('sex')
    unit_query = request.GET.get('unit')
    
    filters = Q()
    if last_name_query:
        filters &= Q(LAST_NAME__icontains=last_name_query)
    if first_name_query:
        filters &= Q(FIRST_NAME__icontains=first_name_query)
    if middle_name_query:
        filters &= Q(MIDDLE_NAME__icontains=middle_name_query)
    if suffix_query and suffix_query != "Suffix":
        filters &= Q(EXTENSION_NAME__icontains=suffix_query)
    if afsn_query:
        filters &= Q(SERIAL_NUMBER__icontains=afsn_query)  # Change this to 'SERIAL_NUMBER'
    if rank_query and rank_query != "Rank":
        filters &= Q(RANK__icontains=rank_query)
    if classification_query and classification_query != "Classification":
        filters &= Q(CLASSIFICATION__icontains=classification_query)
    if sex_query and sex_query != "Sex":
        filters &= Q(SEX__icontains=sex_query)
    if unit_query:
        filters &= Q(UNIT__icontains=unit_query)
    
    persons = PersonnelItem.objects.filter(filters)
    
    paginator = Paginator(persons, 10)
    page_num = request.GET.get("page")
    persons = paginator.get_page(page_num)
    
    return render(request, 'myapp/index.html', {
        'persons': persons,
        'last_name_query': last_name_query,
        'first_name_query': first_name_query,
        'middle_name_query': middle_name_query,
        'suffix_query': suffix_query,
        'afsn_query': afsn_query,
        'rank_query': rank_query,
        'classification_query': classification_query,
        'sex_query': sex_query,
        'unit_query': unit_query,
    })

def Personnel_Records(request):
    last_name_query = request.GET.get('last_name')
    first_name_query = request.GET.get('first_name')
    middle_name_query = request.GET.get('middle_name')
    suffix_query = request.GET.get('suffix')
    afsn_query = request.GET.get('afsn')
    rank_query = request.GET.get('rank')
    classification_query = request.GET.get('classification')
    sex_query = request.GET.get('sex')
    unit_query = request.GET.get('unit')
    
    filters = Q()
    if last_name_query:
        filters &= Q(LAST_NAME__icontains=last_name_query)
    if first_name_query:
        filters &= Q(FIRST_NAME__icontains=first_name_query)
    if middle_name_query:
        filters &= Q(MIDDLE_NAME__icontains=middle_name_query)
    if suffix_query and suffix_query != "Suffix":
        filters &= Q(EXTENSION_NAME__icontains=suffix_query)
    if afsn_query:
        filters &= Q(SERIAL_NUMBER__icontains=afsn_query)  # Change this to 'SERIAL_NUMBER'
    if rank_query and rank_query != "Rank":
        filters &= Q(RANK__icontains=rank_query)
    if classification_query and classification_query != "Classification":
        filters &= Q(CLASSIFICATION__icontains=classification_query)
    if sex_query and sex_query != "Sex":
        filters &= Q(SEX__icontains=sex_query)
    if unit_query:
        filters &= Q(UNIT__icontains=unit_query)
    
    persons = PersonnelItem.objects.filter(filters)
    
    paginator = Paginator(persons, 10)
    page_num = request.GET.get("page")
    persons = paginator.get_page(page_num)
    
    return render(request, 'Base/sidebar.html', {
        'persons': persons,
        'last_name_query': last_name_query,
        'first_name_query': first_name_query,
        'middle_name_query': middle_name_query,
        'suffix_query': suffix_query,
        'afsn_query': afsn_query,
        'rank_query': rank_query,
        'classification_query': classification_query,
        'sex_query': sex_query,
        'unit_query': unit_query,
    })






