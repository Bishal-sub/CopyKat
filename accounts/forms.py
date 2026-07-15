from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class StudentRegisterForm(UserCreationForm):

    class Meta:
        model = User

        fields = [
            'username',
            'full_name',
            'email',
            'phone_number',
            'admission_year',
            'photo',
            'password1',
            'password2',
        ]