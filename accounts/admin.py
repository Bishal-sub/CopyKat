from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    list_display = (
        "username",
        "full_name",
        "role",
        "subject",
        "semester",
        "email",
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
                    "subject",
                    "semester",
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
                    "subject",
                    "semester",
                )
            },
        ),
    )