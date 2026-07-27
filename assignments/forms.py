from django import forms
from .models import Assignment


class AssignmentForm(forms.ModelForm):

    class Meta:

        model = Assignment

        fields = [
            "title",
            "teacher",
            "level",
            "semester",
            "file",
        ]

    def clean_file(self):

        file = self.cleaned_data.get(
            "file"
        )

        if not file:

            raise forms.ValidationError(
                "Please upload a file."
            )

        allowed_extensions = [
            ".pdf",
            ".doc",
            ".docx",
        ]

        filename = file.name.lower()

        if not any(
            filename.endswith(ext)
            for ext in allowed_extensions
        ):

            raise forms.ValidationError(
                "Only PDF, DOC and DOCX files are allowed."
            )

        max_size = 10 * 1024 * 1024

        if file.size > max_size:

            raise forms.ValidationError(
                "File size cannot exceed 10MB."
            )

        return file