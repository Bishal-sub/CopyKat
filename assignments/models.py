from django.db import models
from accounts.models import User
import os


class Assignment(models.Model):

    LEVEL_CHOICES = (
        ("bachelor", "Bachelor"),
        ("master", "Master"),
    )

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    )

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="student_assignments"
    )

    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="teacher_assignments",
        limit_choices_to={"role": "teacher"}
    )

    title = models.CharField(
        max_length=200
    )

    level = models.CharField(
        max_length=20,
        choices=LEVEL_CHOICES
    )

    semester = models.PositiveIntegerField()

    file = models.FileField(
        upload_to="assignments/"
    )

    submitted_at = models.DateTimeField(
        auto_now_add=True
    )

    similarity_percentage = models.FloatField(
        default=0
    )

    teacher_remark = models.TextField(
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    reviewed_at = models.DateTimeField(
        blank=True,
        null=True
    )

    class Meta:
        ordering = ["-submitted_at"]

    def __str__(self):
        return self.title

    @property
    def filename(self):
        return os.path.basename(self.file.name)