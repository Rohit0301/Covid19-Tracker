
from django.urls import path

from . import views

urlpatterns = [
    path("", views.stateWise, name="tracks"),
    path("district/", views.DistrictWise, name="district"),
    path("global/",views.globalD,name="global"),
    path("news/",views.News,name="news")
]