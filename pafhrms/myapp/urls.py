from django.urls import path
from . import views

urlpatterns = [
     path("<int:id>",views.index,name="index"),
    
     path("",views.Personnel_Records,name="Personnel_Records"),
     path(">",views.Placement,name="Placement"),
]