from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, StudentDetails, TeacherAssignment


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "full_name", "role", "email", "phone_number", "is_staff")

    fieldsets = UserAdmin.fieldsets + (
        (
            "Additional Information",
            {
                "fields": (
                    "role",
                    "full_name",
                    "phone_number",
                    "admission_year",
                    "department",
                    "level",
                    "photo",
                    "first_login",
                ),
            },
        ),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Additional Information",
            {
                "fields": (
                    "role",
                    "full_name",
                    "email",
                    "phone_number",
                    "admission_year",
                    "department",
                    "level",
                    "photo",
                ),
            },
        ),
    )

    search_fields = ("username", "full_name", "email", "phone_number")
    list_filter = ("role", "department", "level", "is_staff")


@admin.register(TeacherAssignment)
class TeacherAssignmentAdmin(admin.ModelAdmin):
    list_display = ("teacher", "subject", "department_display", "level", "semester_display")
    list_filter = ("level", "subject__department", "subject__semester")
    search_fields = ("teacher__username", "teacher__full_name", "subject__name")
    ordering = ("subject__semester", "subject__name")

    @admin.display(description="Department", ordering="subject__department__name")
    def department_display(self, obj):
        if obj.subject and obj.subject.department:
            return obj.subject.department.name
        return "-"

    @admin.display(description="Semester", ordering="subject__semester")
    def semester_display(self, obj):
        if obj.subject:
            return obj.subject.semester
        return "-"


@admin.register(StudentDetails)
class StudentDetailsAdmin(admin.ModelAdmin):
    list_display = ("full_name", "admission_year", "barcode_number", "is_registered")
    list_filter = ("admission_year", "is_registered")
    search_fields = ("full_name", "barcode_number")
    ordering = ("-admission_year", "full_name")