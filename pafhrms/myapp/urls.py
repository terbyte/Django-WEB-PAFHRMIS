from django.urls import path
from . import views

from django.conf.urls import handler404

urlpatterns = [
    # path("<int:id>/", views.index, name="index"),
    path('', views.index, name='index'),
    
    path('upload/', views.upload_file, name='upload_file'),
    path('Personnel_Records/', views.Personnel_Records, name='Personnel_Records'),

    path('display/', views.display_data, name='display_data'),
    path('placement/', views.Placement, name='Placement'),
    # path('search/', views.searchpersonnel, name='searchpersonnel'),
]


