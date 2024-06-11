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
import pandas as pd
from datetime import datetime
from .forms import PersonnelItemForm
from .models import Placement
from django.http import HttpResponseBadRequest, HttpResponse
from datetime import datetime, timedelta

def calculate_due_date(duration):
    if duration == '6 Months':
        return datetime.now() + timedelta(weeks=26)
    elif duration == '1 Year':
        return datetime.now() + timedelta(weeks=52)
    elif duration == '2 Years':
        return datetime.now() + timedelta(weeks=104)
    return None

def save_placement_update(request):
    if request.method == 'POST':
        personnel_id = request.POST.get('personnel_id')
        last_name = request.POST.get('last_name')
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name')
        suffix = request.POST.get('suffix')
        new_unit = request.POST.get('new_unit')
        reassignment_date = request.POST.get('reassignmentDate')
        assignment_category = request.POST.get('assignmentcategory')
        duration = request.POST.get('duration')
        upload_file = request.FILES.get('uploadOrder')  # Correct variable name


        print("Durationnnnn")

        if 'uploadOrder' in request.FILES:
            upload_file = request.FILES['uploadOrder']
        else:
            print("No file uploaded")

        # Calculate the due date based on the duration
        reassignment_effective_date_until = calculate_due_date(duration)

        # Create the Placement instance
        placement = Placement(
            AFPSN=personnel_id,
            LAST_NAME=last_name,
            FIRST_NAME=first_name,
            MIDDLE_NAME=middle_name,
            SUFFIX=suffix,
            NEW_UNIT=new_unit,
            REASSIGN_EFFECTIVEDDATE=reassignment_date,
            ASSIGN_CATEGORY=assignment_category,
            REASSIGN_EFFECTIVEDDATE_UNTIL=reassignment_effective_date_until,
            ORDER_UPLOADFILE=upload_file
        )
        placement.save()

        return HttpResponse('Data uploaded successfully.')

    return render(request, 'Placement-modal.html')


# def placement_update_officer(request):
#     print("==================called===========================================")



def Tranche(request):
    return render(request, 'reenlistment/Tranche.html')
 

def format_date(date):
    if date:
        try:
            return datetime.strptime(date, '%Y-%m-%d').date()
        except ValueError:
            # Handle the case where the date format is incorrect
            return None
    return None


def update_personnel(request):
    if request.method == 'POST':
        print("fullreeenlistment",request.POST.get('fullreeenlistment'))
        print("himmmmmmmmmmmmmmmmmmmmmmmmm",request.POST.get('dateoflastetadsot'))
        try:
            personnel_id = request.POST.get('personnel_id')
            personnel_items = PersonnelItem.objects.filter(SERIAL_NUMBER=personnel_id)
            if not personnel_items.exists():
                return JsonResponse({'success': False, 'error': 'Personnel not found'})

            
            personnel_items.update(
                LAST_NAME=request.POST.get('last_name'),
                FIRST_NAME=request.POST.get('first_name'),
                MIDDLE_NAME=request.POST.get('middle_name'),
                EXTENSION_NAME=request.POST.get('suffix'),
                ADDRESS=request.POST.get('address'),
                RANK=request.POST.get('rank'),
                AFSC=request.POST.get('afsc'),
                UNIT=request.POST.get('unit'),
                SUB_UNIT=request.POST.get('subunit'),
                CONTACT_NUMBER=request.POST.get('contactnum'),
                HIGHEST_PME_COURSES=request.POST.get('hpme'),
                PILOT_RATED_NON_RATED=request.POST.get('pilotrating'),
                DATE_LAST_PROMOTION_APPOINTMENT=request.POST.get('promotion'),
                DATE_LASTFULL_REENLISTMENT=format_date(request.POST.get('fullreeenlistment')),
                DATE_LAST_ETAD=format_date(request.POST.get('dateoflastetadsot'))
            )
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request'})




def convert_date(date_value):
    if pd.isna(date_value):
        return None
    if isinstance(date_value, datetime):
        # If the value is already a datetime object, return it in the desired format
        return date_value.strftime('%Y-%m-%d')
    elif isinstance(date_value, str):
        # If the value is a string, try to parse it
        try:
            return datetime.strptime(date_value, '%d-%m-%Y').strftime('%Y-%m-%d')
        except ValueError:
            return None
    else:
        return None

def upload_excel(request):
    if request.method == 'POST' and request.FILES['excel_file']:
        excel_file = request.FILES['excel_file']
        fs = FileSystemStorage()
        filename = fs.save(excel_file.name, excel_file)
        file_path = fs.path(filename)


        df = pd.read_excel(file_path)
        # Convert the date format
        def convert_date(date_value):
            if pd.isna(date_value):
                return None
            if isinstance(date_value, datetime):
                # If the value is already a datetime object, return it in the desired format
                return date_value.strftime('%Y-%m-%d')
            elif isinstance(date_value, str):
                # If the value is a string, try to parse it
                try:
                    return datetime.strptime(date_value, '%d-%b-%y').strftime('%Y-%m-%d')
                except ValueError:
                    return None
            else:
                return None
        try:
            df = pd.read_excel(file_path)
            for index, row in df.iterrows():
                    PersonnelItem.objects.create(
                    RANK=row.iloc[0],
                    LAST_NAME=row.iloc[1],
                    FIRST_NAME=row.iloc[2],
                    MIDDLE_NAME=row.iloc[3],
                    EXTENSION_NAME=row.iloc[4],
                    SERIAL_NUMBER=row.iloc[5],
                    BOS=row.iloc[6],
                    SEX=row.iloc[7],
                    BIRTHDAY=convert_date(row.iloc[8]),
                    CONTACT_NUMBER=row.iloc[9],
                    ADDRESS=row.iloc[10],
                    CLASSIFICATION=row.iloc[11],
                    CATEGORY=row.iloc[12],
                    SOURCE_OF_ENLISTMENT_COMMISION=row.iloc[13],
                    PILOT_RATED_NON_RATED=row.iloc[14],
                    AFSC=row.iloc[15],
                    HIGHEST_PME_COURSES=row.iloc[16],
                    EFFECTIVE_DATE_APPOINTMENT=convert_date(row.iloc[17]),
                    EFFECTIVE_DATE_ENTERED=convert_date(row.iloc[18]),
                    DATE_LAST_PROMOTION_APPOINTMENT=convert_date(row.iloc[19]),
                    UNIT=row.iloc[20],
                    SUB_UNIT=row.iloc[21],
                    DATE_LASTFULL_REENLISTMENT=convert_date(row.iloc[22]),
                    DATE_LAST_ETAD=convert_date(row.iloc[23])
                )
            return HttpResponse('Data uploaded successfully.')
        except Exception as e:
            return HttpResponse(f'Error: {e}')
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
    # return render(request,"myapp/testSidebar.html",{})




def inactivepersonnel(request):
    return render(request,"myapp/InactivePersonnel.html",{})



def display_file_data(request):
    if request.method == 'GET':
        form = UploadFileForm(request.GET, request.FILES)
        


def index(request):
    last_name_query = request.GET.get('last_name')
    first_name_query = request.GET.get('first_name')
    middle_name_query = request.GET.get('middle_name')
    suffix_query = request.GET.get('suffix')
    afsn_query = request.GET.get('afsn')
    rank_query = request.GET.get('rank')
    category_query = request.GET.get('category')
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
    if category_query and category_query != "Category":
        filters &= Q(CATEGORY__icontains=category_query)
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
        'category_query': category_query,
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






# from .models import AFSC

# def autocomplete_afsc(request):
#     if 'term' in request.GET:
#         qs = AFSC.objects.filter(code__icontains=request.GET.get('term'))
#         codes = list(qs.values_list('code', flat=True))
#         return JsonResponse(codes, safe=False)
#     return JsonResponse([])





# PLACEMENT
# FOR OFFICER
def placement_officer(request):
    last_name_query = request.GET.get('last_name')
    first_name_query = request.GET.get('first_name')
    middle_name_query = request.GET.get('middle_name')
    suffix_query = request.GET.get('suffix')
    afsn_query = request.GET.get('afsn')
    rank_query = request.GET.get('rank')
    category_query = ('Officer')
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
        filters &= Q(SERIAL_NUMBER__icontains=afsn_query)  
    if rank_query and rank_query != "Rank":
        filters &= Q(RANK__icontains=rank_query)
    if category_query and category_query:
        filters &= Q(CATEGORY__icontains=category_query)
    if sex_query and sex_query != "Sex":
        filters &= Q(SEX__icontains=sex_query)
    if unit_query:
        filters &= Q(UNIT__icontains=unit_query)
    
    persons = PersonnelItem.objects.filter(filters)
    
    paginator = Paginator(persons, 10)
    page_num = request.GET.get("page")
    persons = paginator.get_page(page_num)
    
    return render(request, 'Placement/placement.html', {
        'persons': persons,
        'last_name_query': last_name_query,
        'first_name_query': first_name_query,
        'middle_name_query': middle_name_query,
        'suffix_query': suffix_query,
        'afsn_query': afsn_query,
        'rank_query': rank_query,
        'category_query': category_query,
        'sex_query': sex_query,
        'unit_query': unit_query,
    })



# FOR ENLISTED PERSONNEL
def placement_enlisted(request):
    last_name_query = request.GET.get('last_name')
    first_name_query = request.GET.get('first_name')
    middle_name_query = request.GET.get('middle_name')
    suffix_query = request.GET.get('suffix')
    afsn_query = request.GET.get('afsn')
    rank_query = request.GET.get('rank')
    category_query = ('ENLISTED PERSONNEL')
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
        filters &= Q(SERIAL_NUMBER__icontains=afsn_query)  
    if rank_query and rank_query != "Rank":
        filters &= Q(RANK__icontains=rank_query)
    if category_query and category_query:
        filters &= Q(CATEGORY__icontains=category_query)
    if sex_query and sex_query != "Sex":
        filters &= Q(SEX__icontains=sex_query)
    if unit_query:
        filters &= Q(UNIT__icontains=unit_query)
    
    persons = PersonnelItem.objects.filter(filters)
    
    paginator = Paginator(persons, 10)
    page_num = request.GET.get("page")
    persons = paginator.get_page(page_num)
    
    return render(request, 'Placement/placement.html', {
        'persons': persons,
        'last_name_query': last_name_query,
        'first_name_query': first_name_query,
        'middle_name_query': middle_name_query,
        'suffix_query': suffix_query,
        'afsn_query': afsn_query,
        'rank_query': rank_query,
        'category_query': category_query,
        'sex_query': sex_query,
        'unit_query': unit_query,
    })
