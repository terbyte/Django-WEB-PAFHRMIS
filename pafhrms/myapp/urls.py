from django.urls import path
from . import views

from django.conf.urls import handler404

urlpatterns = [
    # path("<int:id>/", views.index, name="index"),
    path('', views.index, name='index'),
    
    path('UploadFile/', views.UploadFile, name='UploadFile'),
    # path('Personnel_Records/', views.Personnel_Records, name='Personnel_Records'),

    path('Inactive_Personnel/', views.inactivepersonnel, name='Inactive_Personnel'),
    path('placementOfficer/', views.placementOfficer, name='placementOfficer'),
    
    # path('search/', views.searchpersonnel, name='searchpersonnel'),
]


