from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models


def validate_admission_year(value):
    current_year = datetime.now().year

    if value < 2000 or value > current_year:
        raise ValidationError("Enter a valid admission year.")


class User(AbstractUser):
    ROLE_CHOICES = (
        ("student", "Student"),
        ("teacher", "Teacher"),
        ("admin", "Admin"),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="student",
    )

    full_name = models.CharField(
        max_length=100,
    )

    email = models.EmailField(
        unique=True,
    )

    phone_regex = RegexValidator(
        regex=r"^\+?\d{10,15}$",
        message="Enter a valid phone number.",
    )

    phone_number = models.CharField(
        max_length=15,
        validators=[phone_regex],
        unique=True,
    )

    admission_year = models.PositiveIntegerField(
        validators=[validate_admission_year],
    )

    photo = models.ImageField(
        upload_to="students/",
        blank=True,
        null=True,
    )

    USERNAME_FIELD = "username"

    REQUIRED_FIELDS = [
        "email",
        "full_name",
        "phone_number",
        "admission_year",
    ]

    def __str__(self):
        return self.username