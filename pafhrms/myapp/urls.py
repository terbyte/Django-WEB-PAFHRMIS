from django.urls import path
from . import views

from django.conf.urls import handler404
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    # path("<int:id>/", views.index, name="index"),
    path('', views.index, name='index'),
    path('upload_excel/', views.upload_excel, name='upload_excel'),
    path('Inactive_Personnel/', views.inactivepersonnel, name='Inactive_Personnel'),
    path('update_personnel/', views.update_personnel, name='update_personnel'),  # Add this line 
    path('Tranche/', views.Tranche, name='Tranche'),  
    
    path('placement/', views.placement_officer, name='placement'),
    path('placement/placement_officer', views.placement_officer, name='placement_officer'),
    path('placement/placement_enlisted', views.placement_enlisted, name='placement_enlisted'),
    path('placement/placement_update', views.save_placement_update, name='placement_update'),
    path('placement/placement_DS', views.placement_DS, name='placement_DS'),
    path('placement/placement_DS_extension', views.placement_update_extension, name='placement_DS_extension'),
    path('placement/update_placement', views.update_placement, name='update_placement'),

    # Unit Records
    path('placement/unit_records', views.unit_records, name='unit_records'),


    

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


