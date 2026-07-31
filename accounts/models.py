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
        null=True,
        blank=True,
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
    ]

    def __str__(self):

        return self.username


class TeacherAssignment(models.Model):

    LEVEL_CHOICES = (
        ("bachelor", "Bachelor"),
        ("master", "Master"),
    )

    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={"role": "teacher"},
        related_name="teaching_assignments",
    )

    subject = models.ForeignKey(
        "assignments.Subject",
        on_delete=models.CASCADE,
        related_name="teacher_assignments",
    )

    semester = models.PositiveIntegerField()

    level = models.CharField(
        max_length=20,
        choices=LEVEL_CHOICES,
    )

    class Meta:

        ordering = [
            "semester",
            "subject__name",
        ]

        unique_together = (
            "teacher",
            "subject",
            "semester",
            "level",
        )

    def __str__(self):

        return (
            f"{self.teacher.full_name} | "
            f"{self.subject.name} | "
            f"Semester {self.semester} | "
            f"{self.get_level_display()}"
        )
