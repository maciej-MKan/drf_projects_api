from django.contrib import admin
from django.db import models
from django.forms import DateInput

from projects_manager.project.models import Project


# Register your models here.
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'start_date', 'end_date', 'status']
    list_filter = ['status']
    search_fields = ['name', 'description']

    formfield_overrides = {
        models.DateField: {'widget': DateInput(attrs={'type': 'date'})},
    }
