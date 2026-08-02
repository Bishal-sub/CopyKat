from datetime import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import (
    User,
    StudentDetails,
)

current_year = datetime.now().year

YEAR_CHOICES = [
    (year, year)
    for year in range(
        2000,
        current_year + 1
    )
]


class StudentRegisterForm(
    UserCreationForm
):

    admission_year = forms.ChoiceField(
        label="Admission Year",
        choices=YEAR_CHOICES,
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        ),
    )

    barcode_number = forms.CharField(
        label="ID Card Barcode",
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter Barcode Number",
            }
        ),
    )

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Password",
            }
        ),
    )

    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Confirm Password",
            }
        ),
    )

    class Meta:

        model = User

        fields = [
            "username",
            "full_name",
            "email",
            "phone_number",
            "admission_year",
            "barcode_number",
            "photo",
            "password1",
            "password2",
        ]

        widgets = {

            "username": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Username",
                }
            ),

            "full_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Full Name",
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Email Address",
                }
            ),

            "phone_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Phone Number",
                }
            ),

            "photo": forms.FileInput(
                attrs={
                    "class": "form-control",
                }
            ),
        }

    def clean_admission_year(self):

        return int(
            self.cleaned_data[
                "admission_year"
            ]
        )

    def clean(self):

        cleaned_data = (
            super().clean()
        )


        admission_year = cleaned_data.get(
            "admission_year"
        )

        barcode_number = cleaned_data.get(
            "barcode_number"
        )

        if not (
            
            admission_year
            and barcode_number
        ):
            return cleaned_data

        verification = (
            StudentDetails.objects.filter(
                admission_year=admission_year,
                barcode_number=barcode_number,
            ).first()
        )

        if not verification:

            raise forms.ValidationError(
                "Incorrect barcode or admission year student information."
            )

        if verification.is_registered:

            raise forms.ValidationError(
                "This student has already registered."
            )

        return cleaned_data

    def save(
        self,
        commit=True
    ):

        user = super().save(
            commit=False
        )

        user.role = "student"

        if commit:

            user.save()

            verification = (
                StudentDetails.objects.get(
                    barcode_number=self.cleaned_data[
                        "barcode_number"
                    ]
                )
            )

            verification.is_registered = True

            verification.save()

        return user