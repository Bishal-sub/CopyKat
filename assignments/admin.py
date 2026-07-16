from django.contrib import admin
from .models import Assignment



@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):


    list_display = (

        "title",
        "student",
        "teacher",
        "level",
        "semester",
        "similarity_percentage",
        "status"

    )