from datetime import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User

current_year = datetime.now().year
YEAR_CHOICES = [(year, year) for year in range(2000, current_year + 1)]


class StudentRegisterForm(UserCreationForm):
    admission_year = forms.ChoiceField(
        label="Admission Year",
        choices=YEAR_CHOICES,
        widget=forms.Select(
            attrs={
                "class": "form-control",
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
        """
        Convert the selected year (string) to an integer so it matches
        the PositiveIntegerField in the User model.
        """
        return int(self.cleaned_data["admission_year"])