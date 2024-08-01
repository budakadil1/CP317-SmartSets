from django.contrib import admin

# Register your models here.
from .models import Card

class CardsAdmin(admin.ModelAdmin):
    fields = ["question", "answer", "owner_set"]

admin.site.register(Card, CardsAdmin)