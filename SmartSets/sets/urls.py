from django.urls import path, include
from . import views

urlpatterns = [
    path('search/', views.search_sets, name='search_sets'),
    path('', views.view_sets, name="sets_home"),
    path('view/<slug:slug>', views.view_single_set, name='view_set'),
    path('mysets/', views.my_sets, name='my_sets'),
    path('createset/', views.create_set, name='create_set'),
    path('edit_set/<slug:slug>', views.edit_set, name='edit_set'),
    path('edit_cards/<slug:slug>', views.edit_cards, name='edit_cards'),
    path('delete_set/<slug:slug>', views.delete_set, name='delete_set')
]