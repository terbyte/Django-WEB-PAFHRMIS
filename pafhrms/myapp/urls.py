from django.urls import path
from . import views

from django.conf.urls import handler404

urlpatterns = [
    # path("<int:id>/", views.index, name="index"),
    path('', views.index, name='index'),
    path('UploadFile/', views.UploadFile, name='UploadFile'),
    path('Inactive_Personnel/', views.inactivepersonnel, name='Inactive_Personnel'),
    path('placementOfficer/', views.placementOfficer, name='placementOfficer'),
    path('placementEnlisted/', views.placementEnlisted, name='placementEnlisted'),
    path('update_personnel/', views.update_personnel, name='update_personnel'),  # Add this line 
    path('Tranche/', views.Tranche, name='Tranche'),  
    

]


