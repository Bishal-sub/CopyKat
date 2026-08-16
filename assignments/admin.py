from django.contrib import admin
from .models import Level, Department, Subject, Assignment


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "semester", "level", "department")
    list_filter = ("level", "department", "semester")
    search_fields = ("name",)


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ("title", "student", "teacher", "subject", "department", "level", "semester", "similarity_percentage", "status", "resubmission_used")
    list_filter = ("subject", "department", "level", "semester", "status")
    search_fields = ("title", "student__username", "teacher__username")
    readonly_fields = ("similarity_percentage", "matched_assignment", "submitted_at")