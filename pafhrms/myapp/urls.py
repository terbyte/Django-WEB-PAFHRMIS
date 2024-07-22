from django.urls import path
from . import views

from django.conf.urls import handler404
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    # path("<int:id>/", views.index, name="index"),
    path('', views.index, name='index'),
    path('upload_excel/', views.upload_excel, name='upload_excel'),
    path('update_personnel/', views.update_personnel, name='update_personnel'),  # Add this line 
    path('Tranche/', views.Tranche, name='Tranche'),  

    # Placement
    path('placement/', views.placement_officer, name='placement'),
    path('placement/placement_officer', views.placement_officer, name='placement_officer'),
    path('placement/placement_enlisted', views.placement_enlisted, name='placement_enlisted'),
    path('placement/placement_update', views.save_placement_update, name='placement_update'),
    path('placement/placement_DS', views.placement_DS, name='placement_DS'),
    path('placement/placement_DS_extension', views.placement_update_extension, name='placement_DS_extension'),
    path('placement/update_placement', views.update_placement, name='update_placement'),
    path('placement/placement_Assign', views.placement_Assign, name='placement_Assign'),
    path('placement/orders/<str:afpsn>/', views.user_files, name='orders'),

    # Unit Monitoring 
    path('Unit_Monitoring/unit_monitoring', views.unit_monitoring, name='unit_monitoring'),
    path('Unit_Monitoring/unit_dashboard', views.inactive_Dashboard, name='unit_dashboard'),

    # Reenlistment
    path('reenlistment/Tranche/', views.Tranche, name='Tranche'),
    path('Tranches/', views.Tranches, name='Tranches'),
    path('Medicalforfullreenlistment/', views.Medicalforfullreenlistment, name='Medicalforfullreenlistment'),
    path('Mforfullreenlistment/', views.Mforfullreenlistment, name='Mforfullreenlistment'),  
    path('placement/', views.placement_officer, name='placement'),

    # INACTIVE
    path('for_Seperation/', views.for_Separation, name='for_Seperation'),
    path('lists_inactive/', views.lists_inactive, name='lists_inactive'),
    path('set_inactive/', views.set_inactive, name='set_inactive'),
    

    # REENLISTMENT
    path('update_reenlistment_date/', views.update_reenlistment_date, name='update_reenlistment_date'),  
    path('get_files/<str:serial_number>/', views.get_files, name='get_files'),




    

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


