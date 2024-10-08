from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from .forms import UploadFileForm
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
from datetime import datetime
from .forms import tbl_PersonnelForm
from django.http import HttpResponseBadRequest, HttpResponse
from datetime import datetime, timedelta
from datetime import datetime
from dateutil.relativedelta import relativedelta
import os
from django.conf import settings  # Import settings
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from .models import PersonnelFile
from .models import *
from django.http import JsonResponse
from django.db.models import Count, Q
from itertools import groupby
from operator import attrgetter
from django.db import transaction #for atomicity


def calculate_due_date(duration,reassignment_date):
    reassignment_date = datetime.strptime(reassignment_date, "%Y-%m-%d")
    if duration == '6 Months':
        return reassignment_date + relativedelta(months=6)
    elif duration == '8 Months':
        return reassignment_date + relativedelta(months=8)
    elif duration == '1 Year':
        return reassignment_date + relativedelta(years=1)
    elif duration == '2 Years':
        return reassignment_date+ relativedelta(years=2)
    elif duration == 'NO DEADLINE':
        return None
    return None 

def display_units(request):
    # Fetch all units from the database
    units_list = UnitsTable.objects.all()
    # Set up pagination
    paginator = Paginator(units_list, 10)  # Show 10 units per page
    page_number = request.GET.get('page')  # Get the page number from the request
    page_obj = paginator.get_page(page_number)  # Get the specific page
    
    # Pass the page object to the template
    return render(request, 'afsc/afsc_Dashboard.html', {'page_obj': page_obj})



def afsc_Dashboard(request):
    # Fetch all units from the database
    units_list = UnitsTable.objects.all()

    # Filter out units where UnitCategory is None, blank, or empty
    filtered_units = units_list.exclude(UnitCategory__in=['', None,'none','None','NONE'])

    # Group the filtered units by UnitCategory
    grouped_units = {}
    for key, group in groupby(filtered_units.order_by('UnitCategory'), key=attrgetter('UnitCategory')):
        grouped_units[key] = list(group)

    # Fetch units where FK_MotherUnit is None (i.e., main units)
    main_units = UnitsTable.objects.filter(FK_MotherUnit__isnull=True).exclude(UnitCategory__in=['', None])

    # Flatten the grouped units list for pagination (but excluding main units)
    flat_units_list = [unit for units in grouped_units.values() for unit in units if unit not in main_units]

    # Set up pagination for main units
    paginator = Paginator(main_units, 10)  # Show 10 units per page
    page_number = request.GET.get('page')  # Get the page number from the request
    page_obj = paginator.get_page(page_number)  # Get the specific page


# for AFSC DATAS
    afscs = tbl_AFSC.objects.all()

#FOR COURSES DATA 
    courses = tbl_CoursesTable.objects.all()
    print("courses are: ",courses)




    return render(request, 'afsc/afsc_Dashboard.html', {
        'grouped_units': grouped_units,
        'page_obj': page_obj,
        'main_units': main_units,

        # afsc
        'afscs': afscs,

        # afsc
        'courses': courses



    })




def user_files(request, afpsn):
    files = Placement.objects.filter(AFPSN=afpsn)
    file_list = [{'name': file.ORDER_UPLOADFILE.name, 'url': file.ORDER_UPLOADFILE.url} for file in files]
    print(" listssssssssssss ",file_list)
    return JsonResponse({'files': file_list})


def save_placement_update(request):
    if request.method == 'POST':
        afpsn = request.POST.get('afpsn')
        rank = request.POST.get('rank')
        last_name = request.POST.get('last_name')
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name', '')  # Default to empty string if not provided
        suffix = request.POST.get('suffix', '')  # Default to empty string if not provided
        unit_id = request.POST.get('unit')
        new_unit_id = request.POST.get('new_unit')
        reassignment_date = request.POST.get('reassignmentDate')
        assignment_category = request.POST.get('assignmentcategory')
        duration = request.POST.get('duration')
        dateeffective_until = request.POST.get('formattedNewDate')
        upload_file = request.FILES.get('uploadOrder')
        
        # Calculate the due date based on the duration
        reassignment_effective_date_until = calculate_due_date(duration, reassignment_date)

        if assignment_category == "Assign":
            reassignment_effective_date_until = reassignment_date
            duration = "None"

        try:
            # Retrieve the personnel and unit instances
            personnel = tbl_Personnel.objects.get(AFPSN=afpsn)
            new_unit = UnitsTable.objects.get(pk=new_unit_id)

            # Create the tbl_PersonnelPlacement instance
            placement = tbl_PersonnelPlacement(
                FK_Personnel=personnel,
                FK_Unit=new_unit,
                AssignmentCategory=assignment_category,
                DateFiled=reassignment_date,
                EffectiveDate=reassignment_date,
                EffectiveUntil=reassignment_effective_date_until,
                Duration=duration,
                UploadedOrder=upload_file
            )
            
            placement.save()

            if upload_file:
                # Construct the folder path
                folder_name = f"{afpsn}_{last_name}"
                category_folder_path = os.path.join(settings.MEDIA_ROOT, folder_name, assignment_category)

                # Create the folders if they don't exist
                if not os.path.exists(category_folder_path):
                    os.makedirs(category_folder_path)

                # Define file path and save the file
                file_path = os.path.join(category_folder_path, upload_file.name)
                with open(file_path, 'wb+') as destination:
                    for chunk in upload_file.chunks():
                        destination.write(chunk)

                # Update the UploadedOrder field in the placement instance
                placement.UploadedOrder = file_path
                placement.save()

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return render(request, 'modals/Placement-modal.html')


def update_placement(request):
    if request.method == 'POST':
        afpsn = request.POST.get('afpsn')
        new_unit = request.POST.get('new_unit')
        category = request.POST.get('category')
        Assign = "Assign"
        print("==============================", category)

        # Archive all instances from Placement
        placements = Placement.objects.filter(AFPSN=afpsn, IS_ARCHIVED=False)
        if not placements.exists():
            return JsonResponse({'error': 'Placement not found'}, status=404)
        for placement in placements:
            placement.IS_ARCHIVED = True
            placement.save()
        
        if category != "Assign":
            print("==============================", category, "DS OR TDY")
            # Archive all instances from Placement again if needed
            placements = Placement.objects.filter(AFPSN=afpsn, IS_ARCHIVED=False)
            if not placements.exists():
                return JsonResponse({'error': 'Placement not found'}, status=404)
            for placement in placements:
                placement.IS_ARCHIVED = True
                placement.save()
        # Update the UNIT in tbl_Personnel if The category is assign
        else:
            personnel_item = tbl_Personnel.objects.get(AFPSN=afpsn)
            personnel_item.Unit = new_unit
            personnel_item.SubUnit = "None"
            personnel_item.save()

        return JsonResponse({'success': 'Placement updated successfully'})
    return JsonResponse({'error': 'Invalid request method'}, status=400)


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
    
    filters = Q(isActive =True)
    if last_name_query:
        filters &= Q(LastName__icontains=last_name_query)
    if first_name_query:
        filters &= Q(FirstName__icontains=first_name_query)
    if middle_name_query:
        filters &= Q(MiddleName__icontains=middle_name_query)
    if suffix_query and suffix_query != "Suffix":
        filters &= Q(NameSuffix__icontains=suffix_query)
    if afsn_query:
        filters &= Q(AFPSN__icontains=afsn_query) 
    if rank_query and rank_query != "Rank":
        filters &= Q(Rank__icontains=rank_query)
    if category_query and category_query != "Category":
        filters &= Q(PersCategory__icontains=category_query)
    if sex_query and sex_query != "Sex":
        filters &= Q(Sex__icontains=sex_query)
    if unit_query:
        filters &= Q(Unit__icontains=unit_query)
    
    persons = tbl_Personnel.objects.filter(filters)


    
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



def get_files(request, serial_number):
    person = tbl_Personnel.objects.get(AFPSN=serial_number)
    files = PersonnelFile.objects.filter(personnel=person)
    file_list = [{'name': f.file.name, 'url': f.file.url} for f in files]
    return JsonResponse({'files': file_list})

@require_POST
def update_reenlistment_date(request):
    serial_number = request.POST['serial_number']
    new_date = request.POST['date_lastfull_reenlistment']
    
    person = tbl_Personnel.objects.get(AFPSN=serial_number)
    person.DateLastFullReenlistment = new_date
    
    if 'pdf_file' in request.FILES:
        file = request.FILES['pdf_file']
        PersonnelFile.objects.create(personnel=person, file=file)
    
    person.save()
    return redirect('Tranche')




def format_date(date):
    if date:
        try:
            return datetime.strptime(date, '%Y-%m-%d').date()
        except ValueError:
            # Handle the case where the date format is incorrect
            return None
    return None

# from django.views.decorators.csrf import csrf_protect
# @csrf_protect
@require_POST
def update_personnel(request):
    try:
        personnel_id = request.POST.get('personnel_id')
        personnel_item = tbl_Personnel.objects.filter(PK_Personnel=personnel_id).first()
        
        if not personnel_item:
            return JsonResponse({'success': False, 'error': 'Personnel not found'})

        personnel_item.LastName = request.POST.get('last_name')
        personnel_item.FirstName = request.POST.get('first_name')
        personnel_item.MiddleName = request.POST.get('middle_name')
        personnel_item.NameSuffix = request.POST.get('suffix')
        personnel_item.Address = request.POST.get('address')
        personnel_item.Rank = request.POST.get('rank')
        personnel_item.AFSC_PRIMARY = request.POST.get('afsc')
        # AFSC_SECONDARY=request.POST.get('afsc'),
        # AFSC_TERTIARY=request.POST.get('afsc'),
        personnel_item.Unit = request.POST.get('unit')
        personnel_item.SubUnit = request.POST.get('subunit')
        personnel_item.ContactNumber = request.POST.get('contactnum')
        personnel_item.HighestPMEcourse = request.POST.get('hpme')
        personnel_item.PilotRated_NonRated = request.POST.get('pilotrating')
        personnel_item.DateLastPromotionAppointment = format_date(request.POST.get('promotion'))
        personnel_item.DateLastFullReenlistment = format_date(request.POST.get('fullreeenlistment'))
        personnel_item.DateLastETAD = format_date(request.POST.get('dateoflastetadsot'))
        
        personnel_item.save()
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})



               


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
    




# def upload_excel(request):
#     if request.method == 'POST' and request.FILES['excel_file']:
#         excel_file = request.FILES['excel_file']
#         fs = FileSystemStorage()
#         filename = fs.save(excel_file.name, excel_file)
#         file_path = fs.path(filename)


#         df = pd.read_excel(file_path)
#         # Convert the date format
#         def convert_date(date_value):
#             if pd.isna(date_value):
#                 return None
#             if isinstance(date_value, datetime):
#                 # If the value is already a datetime object, return it in the desired format
#                 return date_value.strftime('%Y-%m-%d')
#             elif isinstance(date_value, str):
#                 # If the value is a string, try to parse it
#                 try:
#                     return datetime.strptime(date_value, '%d-%b-%y').strftime('%Y-%m-%d')
#                 except ValueError:
#                     return None
#             else:
#                 return None
            
#         # Function to convert strings to uppercase, handling NaN values
#         def to_upper(value):
#             if pd.isna(value):
#                 return ''
#             return str(value).upper()
        
#         try:
#             df = pd.read_excel(file_path)
#             for index, row in df.iterrows():
#                 serial_number = row.iloc[5]
#                 # Check if the entry with the same serial number already exists
#                 if not tbl_Personnel.objects.filter(SERIAL_NUMBER=serial_number).exists():
#                     tbl_Personnel.objects.create(
#                         RANK=row.iloc[0],
#                         LAST_NAME=to_upper(row.iloc[1]),  # Convert to uppercase
#                         FIRST_NAME=to_upper(row.iloc[2]),  # Convert to uppercase
#                         MIDDLE_NAME=to_upper(row.iloc[3]),  # Convert to uppercase
#                         EXTENSION_NAME=to_upper(row.iloc[4]),  # Convert to uppercase
#                         SERIAL_NUMBER=serial_number,
#                         BOS=row.iloc[6],
#                         SEX=row.iloc[7],
#                         BIRTHDAY=convert_date(row.iloc[8]),
#                         CONTACT_NUMBER=row.iloc[9],
#                         ADDRESS=row.iloc[10],
#                         CLASSIFICATION=row.iloc[11],
#                         CATEGORY=row.iloc[12],
#                         SOURCE_OF_ENLISTMENT_COMMISION=row.iloc[13],
#                         PILOT_RATED_NON_RATED=row.iloc[14],
#                         AFSC=row.iloc[15],
#                         HIGHEST_PME_COURSES=row.iloc[16],
#                         EFFECTIVE_DATE_APPOINTMENT=convert_date(row.iloc[17]),
#                         EFFECTIVE_DATE_ENTERED=convert_date(row.iloc[18]),
#                         DATE_LAST_PROMOTION_APPOINTMENT=convert_date(row.iloc[19]),
#                         UNIT=row.iloc[20],
#                         SUB_UNIT=row.iloc[21],
#                         DateLastFullReenlistment=convert_date(row.iloc[22]),
#                         DATE_LAST_ETAD=convert_date(row.iloc[23])
#                     )
#             return HttpResponse('Data uploaded successfully.')
#         except Exception as e:
#             return HttpResponse(f'Error: {e}')
#     return render(request, 'myapp/upload.html')

def custom_404(request, exception):
    return render(request, 'other/404.html', status=404)

# INACTIVE FOR SEPARATION

def for_Separation(request):
    last_name_query = request.GET.get('last_name')
    first_name_query = request.GET.get('first_name')
    middle_name_query = request.GET.get('middle_name')
    suffix_query = request.GET.get('suffix')
    afsn_query = request.GET.get('afsn')
    rank_query = request.GET.get('rank')
    classification_query = request.GET.get('classification')
    sex_query = request.GET.get('sex')
    unit_query = request.GET.get('unit')
    
    filters = Q(IS_ACTIVE =True)
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
    
    persons = tbl_Personnel.objects.filter(filters)
    
    paginator = Paginator(persons, 10)
    page_num = request.GET.get("page")
    persons = paginator.get_page(page_num)
    
    return render(request, 'Inactive/for_Seperation.html', {
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
    

def lists_inactive(request):
    last_name_query = request.GET.get('last_name')
    first_name_query = request.GET.get('first_name')
    middle_name_query = request.GET.get('middle_name')
    suffix_query = request.GET.get('suffix')
    afsn_query = request.GET.get('afsn')
    rank_query = request.GET.get('rank')
    classification_query = request.GET.get('classification')
    sex_query = request.GET.get('sex')
    unit_query = request.GET.get('unit')
    
    filters = Q(IS_ACTIVE =False)
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
    
    persons = tbl_Personnel.objects.filter(filters)
    
    paginator = Paginator(persons, 10)
    page_num = request.GET.get("page")
    persons = paginator.get_page(page_num)
    
    return render(request, 'Inactive/lists_inactive.html', {
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




def set_inactive(request):
    if request.method == 'POST':
        serial_number = request.POST.get('afpsn')
        inactivity_reason = request.POST.get('Inactivitycategory')
        upload_order = request.FILES.get('separation_uploadOrder')

        try:
            person = tbl_Personnel.objects.get(SERIAL_NUMBER=serial_number)
            person.IS_ACTIVE = False  # Set to inactive
            person.INACTIVITY_REASON = inactivity_reason

            if upload_order:
                PersonnelFile.objects.create(personnel=person, file=upload_order)

            person.save()
            response = {'success': True}
        except ObjectDoesNotExist:
            response = {'success': False, 'error': 'Personnel item not found'}
        except Exception as e:
            response = {'success': False, 'error': str(e)}

        return JsonResponse(response)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})



def display_file_data(request):
    if request.method == 'GET':
        form = UploadFileForm(request.GET, request.FILES)
        





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
    
    persons = tbl_Personnel.objects.filter(filters)
    
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



# gets sub units
def get_subunits(request):
    unit_id = request.GET.get('unit_id')
    if unit_id:
        # Fetch subunits where FK_MotherUnit matches the selected unit
        try:
            parent_unit = UnitsTable.objects.get(pk=unit_id)
            subunits = UnitsTable.objects.filter(FK_MotherUnit=parent_unit)
            subunit_list = list(subunits.values('PK_Units', 'UnitName'))
            return JsonResponse({'subunits': subunit_list})
        except UnitsTable.DoesNotExist:
            return JsonResponse({'subunits': []})
    return JsonResponse({'subunits': []})


# PLACEMENT DS/TDY/REASSIGNMENT
# FOR OFFICER
def placement_officer(request):
    last_name_query = request.GET.get('last_name')
    first_name_query = request.GET.get('first_name')
    middle_name_query = request.GET.get('middle_name')
    suffix_query = request.GET.get('suffix')
    afpsn_query = request.GET.get('afpsn')
    rank_query = request.GET.get('rank')
    category_query = 'Officer'
    sex_query = request.GET.get('sex')
    unit_query = request.GET.get('unit')


    filters = Q()
    if last_name_query:
        filters &= Q(LastName__icontains=last_name_query)
    if first_name_query:
        filters &= Q(FirstName__icontains=first_name_query)
    if middle_name_query:
        filters &= Q(MiddleName__icontains=middle_name_query)
    if suffix_query and suffix_query != "Suffix":
        filters &= Q(NameSuffix__icontains=suffix_query)
    if afpsn_query:
        filters &= Q(AFPSN__icontains=afpsn_query)
    if rank_query and rank_query != "Rank":
        filters &= Q(Rank__icontains=rank_query)
    if category_query:
        filters &= Q(PersCategory__icontains=category_query)
    if sex_query and sex_query != "Sex":
        filters &= Q(Sex__icontains=sex_query)
    if unit_query:
        filters &= Q(Unit__icontains=unit_query)

    persons = tbl_Personnel.objects.filter(filters)
    paginator = Paginator(persons, 10)
    page_num = request.GET.get("page")
    persons = paginator.get_page(page_num)

    # Fetch units and sub-units
    units = UnitsTable.objects.filter(FK_MotherUnit__isnull=True)
    sub_units = UnitsTable.objects.filter(FK_MotherUnit__isnull=False)

    return render(request, 'Placement/officerTab.html', {
        'persons': persons,
        'last_name_query': last_name_query,
        'first_name_query': first_name_query,
        'middle_name_query': middle_name_query,
        'suffix_query': suffix_query,
        'afpsn_query': afpsn_query,
        'rank_query': rank_query,
        'category_query': category_query,
        'sex_query': sex_query,
        'unit_query': unit_query,
        'units': units,
        'sub_units': sub_units,
    })



# FOR ENLISTED PERSONNEL
def placement_enlisted(request):
    last_name_query = request.GET.get('last_name')
    first_name_query = request.GET.get('first_name')
    middle_name_query = request.GET.get('middle_name')
    suffix_query = request.GET.get('suffix')
    afpsn_query = request.GET.get('afpsn')
    rank_query = request.GET.get('rank')
    category_query = 'ENLISTED PERSONNEL'
    sex_query = request.GET.get('sex')
    unit_query = request.GET.get('unit')


    filters = Q()
    if last_name_query:
        filters &= Q(LastName__icontains=last_name_query)
    if first_name_query:
        filters &= Q(FirstName__icontains=first_name_query)
    if middle_name_query:
        filters &= Q(MiddleName__icontains=middle_name_query)
    if suffix_query and suffix_query != "Suffix":
        filters &= Q(NameSuffix__icontains=suffix_query)
    if afpsn_query:
        filters &= Q(AFPSN__icontains=afpsn_query)
    if rank_query and rank_query != "Rank":
        filters &= Q(Rank__icontains=rank_query)
    if category_query:
        filters &= Q(PersCategory__icontains=category_query)
    if sex_query and sex_query != "Sex":
        filters &= Q(Sex__icontains=sex_query)
    if unit_query:
        filters &= Q(Unit__icontains=unit_query)

    persons = tbl_Personnel.objects.filter(filters)
    paginator = Paginator(persons, 10)
    page_num = request.GET.get("page")
    persons = paginator.get_page(page_num)

    # Fetch units and sub-units
    units = UnitsTable.objects.filter(FK_MotherUnit__isnull=True)
    sub_units = UnitsTable.objects.filter(FK_MotherUnit__isnull=False)

    return render(request, 'Placement/EpTab.html', {
        'persons': persons,
        'last_name_query': last_name_query,
        'first_name_query': first_name_query,
        'middle_name_query': middle_name_query,
        'suffix_query': suffix_query,
        'afpsn_query': afpsn_query,
        'rank_query': rank_query,
        'category_query': category_query,
        'sex_query': sex_query,
        'unit_query': unit_query,
        'units': units,
        'sub_units': sub_units,
    })





# FOR DS
def placement_DS(request):
    
    rank_query = request.GET.get('rank')
    afpsn_query = request.GET.get('afpsn')
    last_name_query = request.GET.get('last_name')
    first_name_query = request.GET.get('first_name')
    middle_name_query = request.GET.get('middle_name')
    suffix_query = request.GET.get('suffix')
    sex_query = request.GET.get('sex')
    unit_query = request.GET.get('unit')
    
    category_queries = ['Detached Service', 'Temporary Duty']
    
    filters = Q(IsArchived =False)
    if last_name_query:
        filters &= Q(FK_Personnel__LastName__icontains=last_name_query)
    if first_name_query:
        filters &= Q(FK_Personnel__FirstName__icontains=first_name_query)
    if middle_name_query:
        filters &= Q(FK_Personnel__MiddleName__icontains=middle_name_query)
    if suffix_query and suffix_query != "Suffix":
        filters &= Q(FK_Personnel__NameSuffix__icontains=suffix_query)
    if afpsn_query:
        filters &= Q(FK_Personnel__AFPSN__icontains=afpsn_query)
    if rank_query and rank_query != "Rank":
        filters &= Q(FK_Personnel__Rank__icontains=rank_query)
    if sex_query and sex_query != "Sex":
        filters &= Q(FK_Personnel__Sex__icontains=sex_query)
    if unit_query:
        filters &= Q(FK_Unit__UnitName__icontains=unit_query)
    if category_queries:
        filters &= Q(AssignmentCategory__in=category_queries)
    
    persons = tbl_PersonnelPlacement.objects.filter(filters).select_related('FK_Personnel').annotate(

        FirstName=F('FK_Personnel__FirstName'),
        MiddleName=F('FK_Personnel__MiddleName'),
        LastName=F('FK_Personnel__LastName'),
        NameSuffix=F('FK_Personnel__NameSuffix'),
        Rank=F('FK_Personnel__Rank'),
        AFPSN=F('FK_Personnel__AFPSN')
    )
    
    paginator = Paginator(persons, 10)
    page_num = request.GET.get("page")
    persons = paginator.get_page(page_num)
    
    return render(request, 'Placement/placement_DS.html', {
        'persons': persons,
        'last_name_query': last_name_query,
        'first_name_query': first_name_query,
        'middle_name_query': middle_name_query,
        'suffix_query': suffix_query,
        'afpsn_query': afpsn_query,
        'rank_query': rank_query,
        'sex_query': sex_query,
        'unit_query': unit_query,
        'category_query': category_queries,
    })


from django.db.models.functions import Concat
from django.db.models import Q, F, Value
# # PLACEMENT ASSIGN new
def placement_Assign(request):
    last_name_query = request.GET.get('last_name')
    first_name_query = request.GET.get('first_name')
    middle_name_query = request.GET.get('middle_name')
    suffix_query = request.GET.get('suffix')
    afpsn_query = request.GET.get('afsn')
    rank_query = request.GET.get('rank')
    category_query = request.GET.get('category')
    sex_query = request.GET.get('sex')
    unit_query = request.GET.get('unit')

    filters = Q(IsArchived=False)
    if last_name_query:
        filters &= Q(FK_Personnel__LastName__icontains=last_name_query)
    if first_name_query:
        filters &= Q(FK_Personnel__FirstName__icontains=first_name_query)
    if middle_name_query:
        filters &= Q(FK_Personnel__MiddleName__icontains=middle_name_query)
    if suffix_query and suffix_query != "Suffix":
        filters &= Q(FK_Personnel__NameSuffix__icontains=suffix_query)
    if afpsn_query:
        filters &= Q(FK_Personnel__AFPSN__icontains=afpsn_query)
    if rank_query and rank_query != "Rank":
        filters &= Q(FK_Personnel__Rank__icontains=rank_query)
    if category_query and category_query != "Category":
        filters &= Q(FK_Personnel__PersCategory__icontains=category_query)
    if sex_query and sex_query != "Sex":
        filters &= Q(FK_Personnel__Sex__icontains=sex_query)
    if unit_query:
        filters &= Q(FK_Unit__UnitName__icontains=unit_query)

    persons = tbl_PersonnelPlacement.objects.filter(filters).select_related('FK_Personnel').annotate(

        FirstName=F('FK_Personnel__FirstName'),
        MiddleName=F('FK_Personnel__MiddleName'),
        LastName=F('FK_Personnel__LastName'),
        NameSuffix=F('FK_Personnel__NameSuffix'),
        Rank=F('FK_Personnel__Rank'),
        AFPSN=F('FK_Personnel__AFPSN')
    )

    paginator = Paginator(persons, 10)
    page_num = request.GET.get("page")
    persons = paginator.get_page(page_num)

    return render(request, 'Placement/placement_Assign.html', {
        'persons': persons,
        'last_name_query': last_name_query,
        'first_name_query': first_name_query,
        'middle_name_query': middle_name_query,
        'suffix_query': suffix_query,
        'afpsn_query': afpsn_query,
        'rank_query': rank_query,
        'sex_query': sex_query,
        'unit_query': unit_query,
        'category_query': category_query,
    })


# SAVING REASSIGNMENT ON MODAL WHEN ASSINGING TO OTHER UNIT OR DS/TDY
# def save_placement_update(request):
#     if request.method == 'POST':
#         afpsn = request.POST.get('afpsn')
#         rank = request.POST.get('rank')
#         last_name = request.POST.get('last_name')
#         first_name = request.POST.get('first_name')
#         middle_name = request.POST.get('middle_name', '')  # Default to empty string if not provided
#         suffix = request.POST.get('suffix', '')  # Default to empty string if not provided
#         mother_unit = request.POST.get('unit')
#         new_unit = request.POST.get('new_unit')
#         reassignment_date = request.POST.get('reassignmentDate')
#         assignment_category = request.POST.get('assignmentcategory')
#         duration = request.POST.get('duration')
#         dateeffective_until = request.POST.get('formattedNewDate')
#         upload_file = request.FILES.get('uploadOrder')
#         # Calculate the due date based on the duration
#         reassignment_effective_date_until = calculate_due_date(duration, reassignment_date)
#         if assignment_category == "Assign":
#             reassignment_effective_date_until = reassignment_date
#             duration = "None"


#         # Create the folder for saving the file if it doesn't exist
#         folder_name = f"{afpsn}_{last_name}"
#         folder_path = os.path.join(settings.MEDIA_ROOT, folder_name)
#         if not os.path.exists(folder_path):
#             os.makedirs(folder_path)

#         # Save the uploaded file to the designated folder
#         if upload_file:
#             file_path = os.path.join(folder_path, upload_file.name)
#             with open(file_path, 'wb+') as destination:
#                 for chunk in upload_file.chunks():
#                     destination.write(chunk)

#         # Create the Placement instance
#         placement = Placement(
#             AFPSN=afpsn,
#             RANK=rank,
#             LAST_NAME=last_name,
#             FIRST_NAME=first_name,
#             MIDDLE_NAME=middle_name,
#             SUFFIX=suffix,
#             MOTHER_UNIT=mother_unit,
#             NEW_UNIT=new_unit,
#             REASSIGN_EFFECTIVEDDATE=reassignment_date,
#             ASSIGNMENT_CATEGORY=assignment_category,
#             REASSIGN_EFFECTIVEDDATE_UNTIL=reassignment_effective_date_until,
#             DURATION=duration,
#             ORDER_UPLOADFILE=upload_file  # This saves the file path in the database
#         )
#         try:
#             placement.save()
#             return JsonResponse({'success': True})
#         except Exception as e:
#             return JsonResponse({'success': False, 'error': str(e)})

#     return render(request, 'modals/Placement-modal.html')




# def save_placement_update(request):
#     if request.method == 'POST':
#         # Retrieve fields from POST data
#         personnel_id = request.POST.get('personnel_id')  # Use personnel_id for update
#         afpsn = request.POST.get('afpsn')
#         last_name = request.POST.get('last_name')
#         first_name = request.POST.get('first_name')
#         middle_name = request.POST.get('middle_name', '')  # Default to empty string if not provided
#         suffix = request.POST.get('suffix', '')  # Default to empty string if not provided
#         unit_id = request.POST.get('unit')
#         new_unit_id = request.POST.get('new_unit')
#         reassignment_date = request.POST.get('reassignmentDate')
#         assignment_category = request.POST.get('assignmentcategory')
#         duration = request.POST.get('duration')
#         dateeffective_until = request.POST.get('formattedNewDate')
#         upload_file = request.FILES.get('uploadOrder')

#         # Calculate the due date based on the duration
#         reassignment_effective_date_until = calculate_due_date(duration, reassignment_date)

#         if assignment_category == "Assign":
#             reassignment_effective_date_until = reassignment_date
#             duration = "None"

#         try:
#             # Retrieve the personnel and unit instances
#             if personnel_id:
#                 personnel = tbl_Personnel.objects.get(pk=personnel_id)  # Use pk for primary key lookup
#             else:
#                 raise ValueError("Personnel ID is required")

#             new_unit = UnitsTable.objects.get(pk=new_unit_id)

#             # Check if we are updating an existing placement
#             placement, created = tbl_PersonnelPlacement.objects.update_or_create(
#                 FK_Personnel=personnel,
#                 FK_Unit=new_unit,
#                 defaults={
#                     'AssignmentCategory': assignment_category,
#                     'DateFiled': reassignment_date,
#                     'EffectiveDate': reassignment_date,
#                     'EffectiveUntil': reassignment_effective_date_until,
#                     'Duration': duration,
#                     'UploadedOrder': upload_file
#                 }
#             )
            
#             if upload_file:
#                 # Construct the folder path
#                 folder_name = f"{afpsn}_{last_name}"
#                 category_folder_path = os.path.join(settings.MEDIA_ROOT, folder_name, assignment_category)

#                 # Create the folders if they don't exist
#                 if not os.path.exists(category_folder_path):
#                     os.makedirs(category_folder_path)

#                 # Define file path and save the file
#                 file_path = os.path.join(category_folder_path, upload_file.name)
#                 with open(file_path, 'wb+') as destination:
#                     for chunk in upload_file.chunks():
#                         destination.write(chunk)

#                 # Update the UploadedOrder field in the placement instance
#                 placement.UploadedOrder = file_path
#                 placement.save()

#             return JsonResponse({'success': True})
#         except Exception as e:
#             return JsonResponse({'success': False, 'error': str(e)})

#     return render(request, 'modals/Placement-modal.html')



# the only problem here is updating data thru PK in personnel, but it hides PK when inspected in web
def save_placement_update(request):
    if request.method == 'POST':
        personnel_id = request.POST.get('personnel_id')
        afpsn = request.POST.get('afpsn')
        rank = request.POST.get('rank')
        last_name = request.POST.get('last_name')
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name', '')  # Default to empty string if not provided
        suffix = request.POST.get('suffix', '')  # Default to empty string if not provided
        unit_id = request.POST.get('unit')
        subunit_id = request.POST.get('subunit')
        reassignment_date = request.POST.get('reassignmentDate')
        assignment_category = request.POST.get('assignmentcategory')
        duration = request.POST.get('duration')
        dateeffective_until = request.POST.get('formattedNewDate')
        upload_file = request.FILES.get('uploadOrder')
        placement_id = request.POST.get('placement_id')  # Add this to identify the record to update
        mother_unit_name = request.POST.get('mother_unit')

        # Retrieve the primary key of the mother unit based on its name
        mother_unit_id = None
        if mother_unit_name:
            try:
                mother_unit = UnitsTable.objects.get(UnitName=mother_unit_name)
                mother_unit_id = mother_unit.pk
            except UnitsTable.DoesNotExist:
                return JsonResponse({'success': False, 'error': f'Mother unit with name {mother_unit_name} does not exist.'})

        print("Mother Unit ID:", mother_unit_id)
        print("ID:", request.POST)

        # Calculate the due date based on the duration
        reassignment_effective_date_until = calculate_due_date(duration, reassignment_date)

        if assignment_category == "Assign":
            reassignment_effective_date_until = reassignment_date
            duration = "None"

        try:
            # Retrieve the personnel instance
            personnel = tbl_Personnel.objects.get(PK_Personnel=personnel_id)
            new_unit = UnitsTable.objects.get(pk=unit_id)
            subunit = UnitsTable.objects.get(pk=subunit_id) if subunit_id else None

            # Check if we are updating an existing record or creating a new one
            if placement_id:
                # Update existing placement
                placement = tbl_PersonnelPlacement.objects.get(pk=placement_id)
                placement.FK_Personnel = personnel
                placement.FK_Unit = new_unit
                placement.AssigningUnit = new_unit
                placement.Subunit = subunit
                placement.AssignmentCategory = assignment_category
                placement.DateFiled = reassignment_date
                placement.EffectiveDate = reassignment_date
                placement.EffectiveUntil = reassignment_effective_date_until
                placement.Duration = duration
                # Set the MotherUnit field if the primary key is available
                if mother_unit_id:
                    placement.MotherUnit = UnitsTable.objects.get(pk=mother_unit_id)
            else:
                # Create a new placement
                placement = tbl_PersonnelPlacement(
                    FK_Personnel=personnel,
                    FK_Unit=new_unit,
                    AssigningUnit=new_unit,
                    Subunit=subunit,
                    AssignmentCategory=assignment_category,
                    DateFiled=reassignment_date,
                    EffectiveDate=reassignment_date,
                    EffectiveUntil=reassignment_effective_date_until,
                    Duration=duration
                )
                # Set the MotherUnit field if the primary key is available
                if mother_unit_id:
                    placement.MotherUnit = UnitsTable.objects.get(pk=mother_unit_id)

            # Save the placement instance first
            placement.save()

            if upload_file:
                # Construct the folder path
                folder_name = f"{afpsn}_{last_name}"
                category_folder_path = os.path.join(settings.MEDIA_ROOT, folder_name, assignment_category)

                # Create the folders if they don't exist
                if not os.path.exists(category_folder_path):
                    os.makedirs(category_folder_path)

                # Define file path and save the file
                file_path = os.path.join(category_folder_path, upload_file.name)
                with open(file_path, 'wb+') as destination:
                    for chunk in upload_file.chunks():
                        destination.write(chunk)

                # Save the file information to tbl_PersonnelFiles
                tbl_PersonnelFiles.objects.create(
                    PK_PersonnelPlacement=placement,
                    Files=file_path,
                    FK_Personnel=personnel
                )

            return JsonResponse({'success': True})
        except tbl_Personnel.DoesNotExist:
            return JsonResponse({'success': False, 'error': f'Personnel with AFPSN {afpsn} does not exist.'})
        except UnitsTable.DoesNotExist:
            return JsonResponse({'success': False, 'error': f'Unit with ID {unit_id} or Subunit with ID {subunit_id} does not exist.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return render(request, 'modals/Placement-modal.html')

















#  PLACEMENT UPDATING EXTENSION
def placement_update_extension(request):
    if request.method == 'POST':
        afpsn = request.POST.get('afpsn')
        reassignment_date = request.POST.get('reassignmentDate')
        duration = request.POST.get('duration')
        last_name = request.POST.get('last_name')
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name', '')  # Default to empty string if not provided
        suffix = request.POST.get('suffix', '')  # Default to empty string if not provided
        upload_file = request.FILES.get('uploadOrder')
        assignment_category = request.POST.get('PlacementCategory')

        # Debugging information
        print("DURATION AND REASSIGNMENT DATE:", duration, reassignment_date)

        # Create the main folder using the AFPSN and last name
        folder_name = f"{afpsn}_{last_name}"
        folder_path = os.path.join(settings.MEDIA_ROOT, folder_name)

        # Create the assignment category subfolder inside the main folder
        subfolder_path = os.path.join(folder_path, assignment_category)
        if not os.path.exists(subfolder_path):
            os.makedirs(subfolder_path)

        # Save the uploaded file to the assignment category subfolder
        if upload_file:
            file_path = os.path.join(subfolder_path, upload_file.name)
            with open(file_path, 'wb+') as destination:
                for chunk in upload_file.chunks():
                    destination.write(chunk)

        # Confirm file upload status
        if 'uploadOrder' in request.FILES:
            print("File uploaded:", upload_file.name)
        else:
            print("No file uploaded")

        # Calculate the due date based on the duration
        reassignment_effective_date_until = calculate_due_date(duration, reassignment_date)

        try:
            # Retrieve personnel placement by filtering on the related personnel's AFPSN
            personnel_placements = tbl_PersonnelPlacement.objects.filter(FK_Personnel__AFPSN=afpsn)
            if not personnel_placements.exists():
                return JsonResponse({'success': False, 'error': 'Personnel not found'})

            # Update the fields of the personnel placement records
            personnel_placements.update(
                EffectiveUntil=reassignment_effective_date_until,  # Updating the correct field for effective until date
                IsArchived=False  # Assuming you want to unarchive the placement (change this as needed)
            )

            # If a file was uploaded, save it to the tbl_PersonnelFiles
            if upload_file:
                for placement in personnel_placements:
                    tbl_PersonnelFiles.objects.create(
                        PK_PersonnelPlacement=placement,
                        Files=upload_file,
                        FK_Personnel=placement.FK_Personnel
                    )

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request'})


# UNIT MONITORING

def unit_monitoring(request):
    unit_query = request.GET.get('unit')
    sub_unit_query = request.GET.get('sub_unit')

    filters = Q()
    if unit_query and unit_query != "UNIT":
        filters &= Q(Unit__icontains=unit_query)
    if sub_unit_query and sub_unit_query != "SUB UNIT":
        filters &= Q(SubUnit__icontains=sub_unit_query)
    persons = tbl_Personnel.objects.filter(filters)
    paginator = Paginator(persons, 10)
    page_num = request.GET.get("page")
    persons = paginator.get_page(page_num)
    
    return render(request, 'Unit_Monitoring/unit_monitoring.html', {
        'persons': persons,
        'unit_query': unit_query,
        'sub_unit_query': sub_unit_query,
    })



def unit_dashboard(request):
    selected_unit = request.GET.get('selected_unit')


# CHANGE GHQ & HSC TO GHQ
    GUAS_units = [
        'GHQ & HSC', 'PAFHRMC', 'AFPWSSUS', 'NOLCOM', 'SOLCOM', 'WESCOM', 
        'VISCOM', 'WESTMINCOM', 'EASTMINCOM', 'JTF-NCR', 'TOWWEST',
    ]

    ALLPAF_units = [
        'GHQ', 'HPAF', 'PAFHRMC A/U', 'PAFHRMC', 'AFPWSSUS', 'AIBDC', 
        'ADC', 'AMC', 'ACC', 'AETDC', 'ARFC', 'TOWNOL', 'TOWSOL', 
        'TOWCEN', 'TOWWEST', 'TOWEASTMIN', '355AEW', '300AISW', 
        '900AFWG', '950CEWW', 'AFFC', 'AFSSG', 'HSSG', 'PAFCMOG', 
        'NOLCOM', 'SOLCOM', 'WESCOM', 'VISCOM', 'WESTMINCOM', 
        'EASTMINCOM', 'JTF-NCR',
    ]

    PAFHRMC_au = [
        'PAFHRMC A/U'
    ]

    guas_filters = Q()
    ALLPAF_units_filters = Q()
    PAFHRMC_au_filters = Q()

    if selected_unit and selected_unit in GUAS_units:
        guas_filters &= Q(UNIT__exact=selected_unit)

    if selected_unit and selected_unit in ALLPAF_units:
        ALLPAF_units_filters &= Q(UNIT__exact=selected_unit)
    
    if selected_unit and selected_unit in PAFHRMC_au:
        PAFHRMC_au_filters &= Q(UNIT__exact=selected_unit)

    GUAS_unit_counts = (
        tbl_Personnel.objects
        .filter(guas_filters)
        .values('Unit')
        .annotate(
            officers_count=Count('pk', filter=Q(PersCategory='OFFICER')),
            enlisted_count=Count('pk', filter=Q(PersCategory='ENLISTED PERSONNEL'))
        )
    )
    ALLPAF_unit_counts = (
        tbl_Personnel.objects
        .filter(ALLPAF_units_filters)
        .values('Unit')
        .annotate(
            officers_count=Count('pk', filter=Q(PersCategory='OFFICER')),
            enlisted_count=Count('pk', filter=Q(PersCategory='ENLISTED PERSONNEL'))
        )
    )
    PAFHRMC_au_counts = (
        tbl_Personnel.objects
        .filter(PAFHRMC_au_filters)
        .values('Unit')
        .annotate(
            officers_count=Count('pk', filter=Q(PersCategory='OFFICER')),
            enlisted_count=Count('pk', filter=Q(PersCategory='ENLISTED PERSONNEL'))
        )
    )

    # Aggregating assignment categories from Placement model
    placement_counts = (
        Placement.objects
        .values('NEW_UNIT')
        .annotate(
            detached_service_count=Count('pk', filter=Q(ASSIGNMENT_CATEGORY='Detached Service')),
            temporary_duty_count=Count('pk', filter=Q(ASSIGNMENT_CATEGORY='Temporary Duty'))
        )
    )

    # Convert placement counts to a dictionary for easy lookup
    placement_counts_dict = {item['NEW_UNIT']: item for item in placement_counts}

    # Update counts with assignment category data
    def update_counts(unit_counts):
        for unit in unit_counts:
            unit_name = unit['Unit']
            if unit_name in placement_counts_dict:
                unit.update(placement_counts_dict[unit_name])
            else:
                unit['detached_service_count'] = 0
                unit['temporary_duty_count'] = 0

    update_counts(GUAS_unit_counts)
    update_counts(ALLPAF_unit_counts)
    update_counts(PAFHRMC_au_counts)

    return render(request, 'Unit_Monitoring/unit_dashboard.html', {
        'selected_unit': selected_unit,
        'GUAS_units': GUAS_units,
        'GUAS_unit_counts': GUAS_unit_counts,
        'ALLPAF_units': ALLPAF_units,
        'ALLPAF_unit_counts': ALLPAF_unit_counts,
        'PAFHRMC_au': PAFHRMC_au,
        'PAFHRMC_au_counts': PAFHRMC_au_counts,
    })


# REENLISTMENT
# For DATE OF NEXT FULL REENLISTMENT
def Tranche(request):
    category_query = 'ENLISTED PERSONNEL'
    unit_query = request.GET.get('unit')
    sub_unit_query = request.GET.get('sub_unit')
    dnfr_query = request.GET.get('dnfr')

    filters = Q()
    if category_query:
        filters &= Q(PersCategory__icontains=category_query)
    if unit_query and unit_query != "UNIT":
        filters &= Q(Unit__icontains=unit_query)
    if sub_unit_query and sub_unit_query != "SUB UNIT":
        filters &= Q(SubUnit__icontains=sub_unit_query)

    persons = tbl_Personnel.objects.filter(filters)

    # Calculate DATE OF NEXT FULL REENLISTMENT
    for person in persons:
        if person.DateLastFullReenlistment:
            person.DATE_NEXTFULL_REENLISTMENT = person.DateLastFullReenlistment + timedelta(days=6*365)  # Roughly adding 6 years

    if dnfr_query and dnfr_query != "YEAR":
        try:
            dnfr_year = int(dnfr_query)
            persons = [person for person in persons if person.DATE_NEXTFULL_REENLISTMENT and person.DATE_NEXTFULL_REENLISTMENT.year == dnfr_year]
        except ValueError:
            # Handle the case where dnfr_query is not a valid integer
            persons = []  # or handle this scenario appropriately

    paginator = Paginator(persons, 10)
    page_num = request.GET.get("page")
    persons = paginator.get_page(page_num)

    return render(request, 'reenlistment/Tranche.html', {
        'persons': persons,
        'category_query': category_query,
        'unit_query': unit_query,
        'sub_unit_query': sub_unit_query,
        'dnfr_query': dnfr_query,         
    })



# for DATE OF 2ND TRANCHE
def Tranches(request):
    category_query = 'ENLISTED PERSONNEL'
    unit_query = request.GET.get('unit')
    sub_unit_query = request.GET.get('sub_unit')
    dnfr_query = request.GET.get('dnfr')

    filters = Q()
    if category_query:
        filters &= Q(PersCategory__icontains=category_query)
    if unit_query and unit_query != "UNIT":
        filters &= Q(Unit__icontains=unit_query)
    if sub_unit_query and sub_unit_query != "SUB UNIT":
        filters &= Q(SubUnit__icontains=sub_unit_query)

    persons = tbl_Personnel.objects.filter(filters)

    # Calculate DATE OF NEXT FULL REENLISTMENT
    for person in persons:
        if person.DateLastFullReenlistment:
            person.DATE_NEXTFULL_REENLISTMENT = person.DateLastFullReenlistment + timedelta(days=3*365)  # Roughly adding 6 years

    if dnfr_query and dnfr_query != "YEAR":
        try:
            dnfr_year = int(dnfr_query)
            persons = [person for person in persons if person.DATE_NEXTFULL_REENLISTMENT and person.DATE_NEXTFULL_REENLISTMENT.year == dnfr_year]
        except ValueError:
            # Handle the case where dnfr_query is not a valid integer
            persons = []  # or handle this scenario appropriately

    paginator = Paginator(persons, 10)
    page_num = request.GET.get("page")
    persons = paginator.get_page(page_num)

    return render(request, 'reenlistment/Tranches.html', {
        'persons': persons,
        'category_query': category_query,
        'unit_query': unit_query,
        'sub_unit_query': sub_unit_query,
        'dnfr_query': dnfr_query,         
    })


#for MEDICAL FOR 2ND TRANCHE
def Medicalforfullreenlistment(request):
    category_query = 'ENLISTED PERSONNEL'
    unit_query = request.GET.get('unit')
    sub_unit_query = request.GET.get('sub_unit')
    dnfr_query = request.GET.get('dnfr')

    filters = Q()
    if category_query:
        filters &= Q(PersCategory__icontains=category_query)
    if unit_query and unit_query != "UNIT":
        filters &= Q(Unit__icontains=unit_query)
    if sub_unit_query and sub_unit_query != "SUB UNIT":
        filters &= Q(SubUnit__icontains=sub_unit_query)

    persons = tbl_Personnel.objects.filter(filters)

    # Calculate DATE OF NEXT FULL REENLISTMENT
    for person in persons:
        if person.DateLastFullReenlistment:
            person.DATE_NEXTFULL_REENLISTMENT = person.DateLastFullReenlistment + timedelta(days=2*365)  # Roughly adding 6 years

    if dnfr_query and dnfr_query != "YEAR":
        try:
            dnfr_year = int(dnfr_query)
            persons = [person for person in persons if person.DATE_NEXTFULL_REENLISTMENT and person.DATE_NEXTFULL_REENLISTMENT.year == dnfr_year]
        except ValueError:
            # Handle the case where dnfr_query is not a valid integer
            persons = []  # or handle this scenario appropriately

    paginator = Paginator(persons, 10)
    page_num = request.GET.get("page")
    persons = paginator.get_page(page_num)

    return render(request, 'reenlistment/Medicalforfullreenlistment.html', {
        'persons': persons,
        'category_query': category_query,
        'unit_query': unit_query,
        'sub_unit_query': sub_unit_query,
        'dnfr_query': dnfr_query,         
    })



#MEDICAL FOR FULL REENLISTMENT
def Mforfullreenlistment(request):
    category_query = 'ENLISTED PERSONNEL'
    unit_query = request.GET.get('unit')
    sub_unit_query = request.GET.get('sub_unit')
    dnfr_query = request.GET.get('dnfr')

    filters = Q()
    if category_query:
        filters &= Q(PersCategory__icontains=category_query)
    if unit_query and unit_query != "UNIT":
        filters &= Q(Unit__icontains=unit_query)
    if sub_unit_query and sub_unit_query != "SUB UNIT":
        filters &= Q(SubUnit__icontains=sub_unit_query)

    persons = tbl_Personnel.objects.filter(filters)

    # Calculate DATE OF NEXT FULL REENLISTMENT
    for person in persons:
        if person.DateLastFullReenlistment:
            person.DATE_NEXTFULL_REENLISTMENT = person.DateLastFullReenlistment + timedelta(days=5*365)  # Roughly adding 6 years

    if dnfr_query and dnfr_query != "YEAR":
        try:
            dnfr_year = int(dnfr_query)
            persons = [person for person in persons if person.DATE_NEXTFULL_REENLISTMENT and person.DATE_NEXTFULL_REENLISTMENT.year == dnfr_year]
        except ValueError:
            # Handle the case where dnfr_query is not a valid integer
            persons = []  # or handle this scenario appropriately

    paginator = Paginator(persons, 10)
    page_num = request.GET.get("page")
    persons = paginator.get_page(page_num)

    return render(request, 'reenlistment/Mforfullreenlistment.html', {
        'persons': persons,
        'category_query': category_query,
        'unit_query': unit_query,
        'sub_unit_query': sub_unit_query,
        'dnfr_query': dnfr_query,         
    })











# UPLOADS

def upload_excel(request):
    if request.method == 'POST' and request.FILES.get('excel_file'):
        excel_file = request.FILES['excel_file']
        fs = FileSystemStorage()
        filename = fs.save(excel_file.name, excel_file)
        file_path = fs.path(filename)

        # Function to convert date format
        def convert_date(date_value):
            if pd.isna(date_value):
                return None
            if isinstance(date_value, datetime):
                return date_value.strftime('%Y-%m-%d')
            elif isinstance(date_value, str):
                # Attempt to parse common date formats
                for fmt in ('%d-%b-%y', '%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y'):
                    try:
                        return datetime.strptime(date_value, fmt).strftime('%Y-%m-%d')
                    except ValueError:
                        continue
            return None

        # Function to convert strings to uppercase, handling NaN values
        def to_upper(value):
            if pd.isna(value):
                return ''
            return str(value).upper()

        try:
            df = pd.read_excel(file_path)
            
            # Print columns for debugging
            print("Columns in Excel file:", df.columns)

            # Begin atomic transaction
            with transaction.atomic():
                # Iterate over each row in the DataFrame
                for index, row in df.iterrows():
                    # Use row.get() to avoid KeyError if the column is missing
                    afpsn = row.get('SERIAL NUMBER', '')

                    # Check if the entry with the same AFPSN already exists
                    if not tbl_Personnel.objects.filter(AFPSN=afpsn).exists():
                        tbl_Personnel.objects.create(
                            FirstName=to_upper(row.get('FIRST NAME', '')),
                            MiddleName=to_upper(row.get('MIDDLE NAME', '')),
                            LastName=to_upper(row.get('LAST NAME', '')),
                            NameSuffix=to_upper(row.get('SUFFIX', '')),
                            AFPSN=afpsn,
                            Rank=row.get('RANK', ''),
                            BOS=row.get('BOS', ''),
                            Sex=row.get('SEX', ''),
                            Birthday=convert_date(row.get('BIRTHDAY', '')),
                            ContactNumber=row.get('CONTACT NUMBER', ''),
                            EmailAddress=row.get('EMAIL ADDRESS', ''),
                            Address=row.get('ADDRESS', ''),
                            Classification=row.get('CLASSIFICATION', ''),
                            PersCategory=row.get('PERS CATEGORY', ''),
                            SourceOfCommissionEnlistment=row.get('SOURCE OF COMMISSION/ENLISTMENT', ''),
                            PilotRated_NonRated=row.get('PILOT (RATED / NON-RATED)', ''),
                            AFSC_PRIMARY=row.get('PRIMARY AFSC', ''),
                            AFSC_SECONDARY=row.get('SECONDARY AFSC', ''),
                            AFSC_TERTIARY=row.get('TERTIARY AFSC', ''),
                            HighestPMEcourse=row.get('HIGHEST PME COURSES', ''),
                            EffectiveDateOfAppointment=convert_date(row.get('EFFECTIVE DATE OF APPOINTMENT (CAD)/ DATE GRADUATED PMA/OCS/BMT', '')),
                            DateEnteredMilitary=convert_date(row.get('DATE ENTERED MILITARY SERVICE', '')),
                            DateLastPromotionAppointment=convert_date(row.get('DATE OF LAST PROMOTION / APPOINTMENT', '')),
                            Unit=row.get('UNIT', ''),
                            SubUnit=row.get('SUB UNIT', ''),
                            DateUnitAssigned=convert_date(row.get('DATE UNIT ASSIGNED', '')),
                            DateLastFullReenlistment=convert_date(row.get('DATE OF LAST FULL REENLISTMENT', '')),
                            DateLastETAD=convert_date(row.get('DATE OF LAST ETAD', '')),
                            BachelorsDegree=row.get('BACHELORS DEGREE', ''),
                            HighestAttainment=row.get('HIGHEST ATTAINMENT', ''),
                            SchoolAttended=row.get('SCHOOL ATTENDED', ''),
                            # WithEligibility=row.get('WithEligibility', ''),
                            EligibilityDescription=row.get('ELIGIBILITY', ''),
                            isActive=True  # Default value
                        )
            return HttpResponse('Data uploaded successfully.')
        except Exception as e:
            # Print error details for debugging
            print(f'Error: {e}')
            return HttpResponse(f'Error: {e}')
    return render(request, 'myapp/upload.html')




def table_Units_upload(request):
    if request.method == 'POST' and request.FILES.get('excel_file'):
        excel_file = request.FILES['excel_file']
        # Read the file directly from the uploaded file object
        df = pd.read_excel(excel_file)
        # Print DataFrame columns to verify
        print("Columns in Excel file:", df.columns)

        # Function to convert strings to uppercase, handling NaN values
        def to_upper(value):
            if pd.isna(value):
                return ''
            return str(value).upper()

        try:
            with transaction.atomic():
                for index, row in df.iterrows():
                    unit_type = to_upper(row['Unit_Type'])
                    unit_name = to_upper(row['Unit_Name'])
                    unit_description = to_upper(row['Unit_Description'])
                    UnitCategory = to_upper(row['Unit_Category'])
                    unit_under = to_upper(row.get('Unit_Under', ''))

                    # Determine the FK_MotherUnit based on Unit_Type
                    parent_unit = None
                    if unit_type == 'MAIN':
                        parent_unit = None  # MAIN units do not have a parent
                    elif unit_type == 'SUB':
                        if unit_under:
                            try:
                                parent_unit = UnitsTable.objects.get(UnitName=unit_under)
                            except UnitsTable.DoesNotExist:
                                parent_unit = None

                    # Create the unit
                    UnitsTable.objects.create(
                        UnitName=unit_name,
                        UnitDescription=unit_description,
                        UnitCategory=UnitCategory,
                        Logo=row.get('Logo', ''),  # Handle optional Logo field
                        FK_MotherUnit=parent_unit  # Set the foreign key relationship
                    )
            return HttpResponse('Data uploaded successfully.')
        except Exception as e:
            return HttpResponse(f'Error: {e}')
    return render(request, 'myapp/upload.html')



def upload_afsc(request):
    if request.method == 'POST' and request.FILES.get('excel_file'):
        excel_file = request.FILES['excel_file']
        fs = FileSystemStorage()
        filename = fs.save(excel_file.name, excel_file)
        file_path = fs.path(filename)
        # Function to convert strings to uppercase, handling NaN values
        def to_upper(value):
            if pd.isna(value):
                return ''
            return str(value).upper()
        try:
            df = pd.read_excel(file_path)
            # Print columns for debugging
            print("Columns in Excel file:", df.columns)
            # Begin atomic transaction
            with transaction.atomic():
                # Iterate over each row in the DataFrame
                for index, row in df.iterrows():
                    # Use row.get() to avoid KeyError if the column is missing
                    AFSCCODE = row.get('AFSC CODE', '')
                    # Check if the entry with the same AFPSN already exists
                    if not tbl_AFSC.objects.filter(AFSCCode=AFSCCODE).exists():
                        tbl_AFSC.objects.create(
                            AFSCCode=AFSCCODE,
                            AFSCDescription=to_upper(row.get('AFSC DESCRIPTION', '')),
                            AFSCLevel=to_upper(row.get('AFSC LEVEL', '')),
                        )
            return HttpResponse('Data uploaded successfully.')
        except Exception as e:
            # Print error details for debugging
            print(f'Error: {e}')
            return HttpResponse(f'Error: {e}')
    return render(request, 'myapp/upload.html')




def upload_courses(request):
    if request.method == 'POST' and request.FILES.get('excel_file'):
        excel_file = request.FILES['excel_file']
        fs = FileSystemStorage()
        filename = fs.save(excel_file.name, excel_file)
        file_path = fs.path(filename)

        # Function to convert strings to uppercase, handling NaN values
        def to_upper(value):
            if pd.isna(value):
                return ''
            return str(value).upper()

        try:
            df = pd.read_excel(file_path)

            # Print columns for debugging
            print("Columns in Excel file:", df.columns)

            # Ensure the required columns are present
            required_columns = ['COURSE TITLE', 'COURSE DESCRIPTION']
            for col in required_columns:
                if col not in df.columns:
                    raise ValueError(f"Missing required column: {col}")

            # Begin atomic transaction
            with transaction.atomic():
                # Iterate over each row in the DataFrame
                for index, row in df.iterrows():
                    course_title = to_upper(row.get('COURSE TITLE', ''))
                    course_description = to_upper(row.get('COURSE DESCRIPTION', ''))
                    # Check if the entry with the same CourseDescription already exists
                    if not tbl_CoursesTable.objects.filter(CourseDescription=course_description).exists():
                        tbl_CoursesTable.objects.create(
                            CourseTitle=course_title,
                            CourseDescription=course_description,
                        )

            # Optionally, remove the file after processing
            fs.delete(filename)

            return HttpResponse('Data uploaded successfully.')
        except Exception as e:
            # Print error details for debugging
            print(f'Error: {e}')
            return HttpResponse(f'Error: {e}')
    return render(request, 'myapp/upload.html')