from django.urls import path
from . import views

from django.conf.urls import handler404

urlpatterns = [
    # path("<int:id>/", views.index, name="index"),
    path('', views.index, name='index'),
    
    path('UploadFile/', views.UploadFile, name='UploadFile'),
    path('Personnel_Records/', views.Personnel_Records, name='Personnel_Records'),

    path('search_Personnel/', views.search_Personnel, name='search_Personnel'),
    path('placement/', views.Placement, name='Placement'),
    # path('search/', views.searchpersonnel, name='searchpersonnel'),
]


