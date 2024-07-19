from django.urls import path, include
from . import views

urlpatterns = [
    path('search/', views.search_sets, name='search_sets'),
    path('', views.view_sets, name="sets_home"),
    path('view/<slug:slug>', views.view_single_set, name='view_set'),
    path('mysets/', views.my_sets, name='my_sets'),
    path('createset/', views.create_set, name='create_set')
]