from django.urls import path, include
from . import views

urlpatterns = [
    path('add_card/<slug:slug>', views.add_card, name='add_card'),
    path('edit_card/<slug:slug>', views.edit_card, name='edit_card'),
    path('remove_card/<slug:slug>', views.remove_card, name='remove_card'),
]