from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    User,
    TeacherAssignment,
)


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    list_display = (
        "username",
        "full_name",
        "role",
        "email",
        "phone_number",
        "is_staff",
    )

    fieldsets = UserAdmin.fieldsets + (
        (
            "Additional Information",
            {
                "fields": (
                    "role",
                    "full_name",
                    "phone_number",
                    "admission_year",
                    "photo",
                )
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
                    "photo",
                )
            },
        ),
    )


@admin.register(TeacherAssignment)
class TeacherAssignmentAdmin(admin.ModelAdmin):

    list_display = (
        "teacher",
        "subject",
        "semester",
    )

    list_filter = (
        "semester",
        "subject",
    )

    search_fields = (
        "teacher__username",
        "teacher__full_name",
        "subject__name",
    )

    ordering = (
        "semester",
        "subject",
    )