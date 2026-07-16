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
            "file"

        ]


        widgets = {


            "title": forms.TextInput(
                attrs={
                    "class":"form-control"
                }
            ),


            "teacher": forms.Select(
                attrs={
                    "class":"form-control"
                }
            ),


            "level": forms.Select(
                attrs={
                    "class":"form-control"
                }
            ),


            "semester": forms.NumberInput(
                attrs={
                    "class":"form-control"
                }
            ),


            "file": forms.FileInput(
                attrs={
                    "class":"form-control"
                }
            ),

        }