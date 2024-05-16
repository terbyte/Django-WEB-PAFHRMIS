from django.urls import path
from . import views

urlpatterns = [
    path("<int:id>/", views.index, name="index"),
    path('upload/', views.upload_file, name='upload_file'),
    path('side/', views.side, name='side'),

    path('display/', views.display_data, name='display_data'),
    path('personnel-records/', views.Personnel_Records, name='Personnel_Records'),
    path('placement/', views.Placement, name='Placement'),
    # path('search/', views.searchpersonnel, name='searchpersonnel'),
]