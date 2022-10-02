from django.urls import path

from . import views

urlpatterns = [

    path('home/',views.converted),
    path('', views.index, name='index'),
    path("click/", views.clickreport, name="clickreport")
]