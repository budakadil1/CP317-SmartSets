from django.contrib import admin

# Register your models here.
from .models import Sets

class SetsAdmin(admin.ModelAdmin):
    fields = ["name", "description", "card_count", "public", "shared_with", "author", "slug"]

admin.site.register(Sets, SetsAdmin)