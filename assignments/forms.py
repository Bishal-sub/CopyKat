from django import forms

from .models import (
    Assignment,
    Subject,
)


class AssignmentForm(forms.ModelForm):

    class Meta:

        model = Assignment

        fields = (
            "title",
            "subject",
            "level",
            "semester",
            "file",
        )

        widgets = {

            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter assignment title",
                }
            ),

            "subject": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "level": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "semester": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1,
                    "max": 10,
                    "placeholder": "Enter semester",
                }
            ),

            "file": forms.FileInput(
                attrs={
                    "class": "form-control",
                    "accept": ".pdf,.doc,.docx",
                }
            ),
        }

        labels = {

            "title": "Assignment Title",

            "subject": "Subject",

            "level": "Level",

            "semester": "Semester",

            "file": "Assignment File",
        }

    def clean_title(self):

        title = self.cleaned_data.get(
            "title"
        )

        if not title:
            raise forms.ValidationError(
                "Title is required."
            )

        title = title.strip()

        if len(title) < 3:

            raise forms.ValidationError(
                "Title must contain at least 3 characters."
            )

        return title

    def clean_semester(self):

        semester = self.cleaned_data.get(
            "semester"
        )

        if semester is None:

            raise forms.ValidationError(
                "Semester is required."
            )

        if semester < 1:

            raise forms.ValidationError(
                "Semester must be greater than 0."
            )

        if semester > 10:

            raise forms.ValidationError(
                "Semester cannot exceed 10."
            )

        return semester

    def clean_file(self):

        file = self.cleaned_data.get(
            "file"
        )

        if not file:

            raise forms.ValidationError(
                "Please upload a file."
            )

        allowed_extensions = (
            ".pdf",
            ".doc",
            ".docx",
        )

        if not file.name.lower().endswith(
            allowed_extensions
        ):

            raise forms.ValidationError(
                "Only PDF, DOC and DOCX files are allowed."
            )

        max_size = 10 * 1024 * 1024  # 10 MB

        if file.size > max_size:

            raise forms.ValidationError(
                "Maximum file size is 10 MB."
            )

        return file

    def clean(self):

        cleaned_data = super().clean()

        level = cleaned_data.get(
            "level"
        )

        semester = cleaned_data.get(
            "semester"
        )

        if level == "master" and semester:

            if semester > 4:

                raise forms.ValidationError(
                    "Master level only supports semesters 1-4."
                )

        return cleaned_data