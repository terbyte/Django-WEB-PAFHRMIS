from django.urls import path
from . import views

urlpatterns = [
     path("",views.Personnel_Records,name="Personnel_Records")
]