from django.contrib import admin
from .models import Subject, Assignment


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
    )

    search_fields = (
        "name",
    )


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "student",
        "teacher",
        "subject",
        "semester",
        "similarity_percentage",
        "status",
        "resubmission_used",
    )

    list_filter = (
        "subject",
        "semester",
        "status",
        "level",
    )

    search_fields = (
        "title",
        "student__username",
        "teacher__username",
    )

    readonly_fields = (
        "similarity_percentage",
        "matched_assignment",
        "submitted_at",
    )