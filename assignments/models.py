import os

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Level(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=100)
    semester = models.PositiveIntegerField()
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name="subjects", null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="subjects", null=True, blank=True)

    class Meta:
        unique_together = ("name", "semester", "level", "department")
        ordering = ["semester", "name"]

    def __str__(self):
        return f"{self.name} - Semester {self.semester}"


class TeacherTask(models.Model):
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="created_tasks", limit_choices_to={"role": "teacher"})
    batch = models.PositiveIntegerField()
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name="tasks")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="tasks")
    semester = models.PositiveIntegerField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="tasks")
    topic = models.CharField(max_length=255)
    description = models.TextField()
    show_at = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.topic

    @property
    def is_visible(self):
        return timezone.now() >= self.show_at

    @property
    def is_open(self):
        now = timezone.now()
        return self.show_at <= now <= self.due_date

    @property
    def is_overdue(self):
        return timezone.now() > self.due_date

    def clean(self):
        super().clean()

        if self.show_at and self.due_date and self.due_date <= self.show_at:
            raise ValidationError({"due_date": "Due date must be later than the assignment show date."})

        if not self.subject:
            return

        if self.subject.semester != self.semester:
            raise ValidationError({"subject": "Selected subject does not belong to the selected semester."})

        if self.subject.department_id != self.department_id:
            raise ValidationError({"subject": "Selected subject does not belong to the selected department."})

        if self.subject.level_id != self.level_id:
            raise ValidationError({"subject": "Selected subject does not belong to the selected level."})

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class Assignment(models.Model):
    STATUS_CHOICES = (
        ("not_submitted", "Not Submitted"),
        ("pending_review", "Pending Review"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
        ("resubmission_required", "Resubmission Required"),
        ("final_rejected", "Final Rejected"),
        ("overdue", "Overdue"),
    )

    task = models.ForeignKey(TeacherTask, on_delete=models.CASCADE, related_name="submissions", null=True, blank=True)
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="student_assignments", limit_choices_to={"role": "student"})
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="submitted_assignments_to_review", limit_choices_to={"role": "teacher"})
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="assignments")
    title = models.CharField(max_length=200)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name="assignments", null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="assignments", null=True, blank=True)
    semester = models.PositiveIntegerField(default=1)
    file = models.FileField(upload_to="assignments/")
    submitted_at = models.DateTimeField(auto_now_add=True)
    similarity_percentage = models.CharField(max_length=50, default="0%")
    matched_assignment = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="matched_with")
    matching_text = models.TextField(blank=True, null=True)
    teacher_remark = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="pending_review")
    reviewed_at = models.DateTimeField(blank=True, null=True)
    resubmission_used = models.BooleanField(default=False)
    resubmission_deadline = models.DateTimeField(blank=True, null=True)
    submission_attempt = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["-submitted_at"]

    def __str__(self):
        return self.title

    @property
    def filename(self):
        return os.path.basename(self.file.name) if self.file else ""

    def clean(self):
        super().clean()

        if not self.task:
            return

        if self.student:
            if self.student.admission_year != self.task.batch:
                raise ValidationError({"student": "Student batch does not match the assignment batch."})

            if self.student.department_id != self.task.department_id:
                raise ValidationError({"student": "Student department does not match the assignment department."})

            if self.student.level_id != self.task.level_id:
                raise ValidationError({"student": "Student level does not match the assignment level."})

        if self.teacher_id != self.task.teacher_id:
            raise ValidationError({"teacher": "Assignment teacher does not match the task teacher."})

        if self.subject_id != self.task.subject_id:
            raise ValidationError({"subject": "Assignment subject does not match the task subject."})

        if self.level_id != self.task.level_id:
            raise ValidationError({"level": "Assignment level does not match the task level."})

        if self.department_id != self.task.department_id:
            raise ValidationError({"department": "Assignment department does not match the task department."})

        if self.semester != self.task.semester:
            raise ValidationError({"semester": "Assignment semester does not match the task semester."})

        if self.submission_attempt < 1:
            raise ValidationError({"submission_attempt": "Submission attempt must be at least 1."})

        if self.submission_attempt > 2:
            raise ValidationError({"submission_attempt": "A maximum of 2 submission attempts is allowed."})

        if self.submission_attempt == 2 and not self.resubmission_used:
            raise ValidationError({"resubmission_used": "Second submission must be marked as a resubmission."})

        if self.resubmission_used and self.submission_attempt != 2:
            raise ValidationError({"submission_attempt": "A used resubmission must have submission attempt 2."})

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
