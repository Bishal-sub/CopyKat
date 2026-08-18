from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone


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

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="student")
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    phone_regex = RegexValidator(regex=r"^\+?\d{10,15}$", message="Enter a valid phone number.")
    phone_number = models.CharField(max_length=15, validators=[phone_regex], unique=True)

    admission_year = models.PositiveIntegerField(validators=[validate_admission_year], null=True, blank=True)
    department = models.ForeignKey("assignments.Department", on_delete=models.SET_NULL, null=True, blank=True, related_name="users")
    level = models.ForeignKey("assignments.Level", on_delete=models.SET_NULL, null=True, blank=True, related_name="users")
    barcode_number = models.CharField(max_length=100, unique=True, null=True, blank=True)
    photo = models.ImageField(upload_to="students/", null=True, blank=True)
    first_login = models.BooleanField(default=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "full_name", "phone_number"]

    def __str__(self):
        return self.username

    @property
    def is_student(self):
        return self.role == "student"

    @property
    def is_teacher(self):
        return self.role == "teacher"

    @property
    def is_admin_user(self):
        return self.role == "admin"


class TeacherAssignment(models.Model):
    LEVEL_CHOICES = (
        ("bachelor", "Bachelor"),
        ("master", "Master"),
    )

    teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={"role": "teacher"}, related_name="teaching_assignments")
    subject = models.ForeignKey("assignments.Subject", on_delete=models.CASCADE, related_name="teacher_assignments")
    semester = models.PositiveIntegerField()
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)

    class Meta:
        ordering = ["semester", "subject__name"]
        unique_together = ("teacher", "subject", "semester", "level")

    def __str__(self):
        return f"{self.teacher.full_name} | {self.subject.name} | Semester {self.semester} | {self.get_level_display()}"


class StudentDetails(models.Model):
    full_name = models.CharField(max_length=100)
    admission_year = models.PositiveIntegerField()
    barcode_number = models.CharField(max_length=100, unique=True)
    is_registered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.admission_year})"


class EmailVerificationOTP(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="email_verification_otps")
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=10)

    def __str__(self):
        return f"{self.user.email} - {self.otp}"


class PasswordResetOTP(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="password_reset_otps")
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=10)

    def __str__(self):
        return f"{self.user.username}"