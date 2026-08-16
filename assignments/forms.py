from zoneinfo import ZoneInfo  # Kathmandu ko timezone ko lagi
from django import forms  # Django forms ko lagi
from django.contrib.auth import get_user_model  # User model lina
from django.core.exceptions import ValidationError  # Form validation ko lagi

from .models import Assignment, Department, Level, Subject, TeacherTask  # Required models
from accounts.models import TeacherAssignment  # Teacher ko assigned subjects ko lagi

User = get_user_model()  # Project ko User model lina


class TeacherTaskForm(forms.ModelForm):
    batch = forms.TypedChoiceField(choices=[], coerce=int, required=True, widget=forms.Select(attrs={"class": "form-select"}))  # Batch select garne field

    class Meta:
        model = TeacherTask
        fields = ["batch", "department", "semester", "level", "subject", "topic", "description", "show_at", "due_date"]  # Form ma rakhne fields

        widgets = {
            "department": forms.Select(attrs={"class": "form-select"}),  # Department select garne
            "semester": forms.Select(attrs={"class": "form-select"}),  # Semester select garne
            "level": forms.Select(attrs={"class": "form-select", "readonly": "readonly"}),  # Level manually change garna nadine
            "subject": forms.Select(attrs={"class": "form-select"}),  # Subject select garne
            "topic": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter assignment topic"}),  # Topic input
            "description": forms.Textarea(attrs={"class": "form-control", "placeholder": "Enter assignment instructions...", "rows": 6}),  # Assignment details
            "show_at": forms.DateTimeInput(format="%Y-%m-%dT%H:%M", attrs={"class": "form-control", "type": "datetime-local"}),  # Assignment dekhaune time
            "due_date": forms.DateTimeInput(format="%Y-%m-%dT%H:%M", attrs={"class": "form-control", "type": "datetime-local"}),  # Assignment deadline
        }

    def __init__(self, *args, teacher=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.teacher = teacher  # Current teacher store garne

        batches = User.objects.filter(role="student", admission_year__isnull=False).values_list("admission_year", flat=True).distinct().order_by("-admission_year")  # Available batches nikalne
        self.fields["batch"].choices = [("", "Select Batch")] + [(str(batch), f"Batch {batch}") for batch in batches]  # Batch choices banaune

        self.fields["department"].queryset = Department.objects.all().order_by("name")  # Department haru name anusar dekhaune
        self.fields["department"].empty_label = "Select Department"  # Department ko default option
        self.fields["level"].queryset = Level.objects.all().order_by("name")  # Level haru name anusar dekhaune
        self.fields["level"].empty_label = "Select Level"  # Level ko default option
        self.fields["level"].disabled = True  # Level manually select garna nadine
        self.fields["semester"].choices = [("", "Select Semester")]  # Semester ko default option
        self.fields["subject"].queryset = Subject.objects.none()  # Suruma subject list empty rakhne
        self.fields["subject"].empty_label = "Select Subject"  # Subject ko default option

        self.subject_data = []  # JavaScript ko lagi subject data
        self.department_semester_map = {}  # Department anusar semester store garne

        if teacher:
            assignments = TeacherAssignment.objects.filter(teacher=teacher).select_related("subject", "subject__department")  # Teacher ko assigned subjects nikalne
            subject_ids = assignments.values_list("subject_id", flat=True).distinct()  # Assigned subject IDs nikalne
            subjects = Subject.objects.filter(id__in=subject_ids).select_related("level", "department").order_by("semester", "name")  # Teacher ko subjects nikalne

            for subject in subjects:
                self.subject_data.append({"id": subject.id, "name": subject.name, "semester": subject.semester, "level_id": subject.level_id, "department_id": subject.department_id})  # Subject details store garne

                if subject.department_id:
                    department_id = str(subject.department_id)  # Department ID string ma rakhne

                    if department_id not in self.department_semester_map:
                        self.department_semester_map[department_id] = set()  # Department ko semesters rakhne

                    self.department_semester_map[department_id].add(subject.semester)  # Semester add garne

        for department_id in self.department_semester_map:
            self.department_semester_map[department_id] = sorted(self.department_semester_map[department_id])  # Semester sort garne

        if self.is_bound:
            department_id = self.data.get("department")  # Submitted department lina
            semester = self.data.get("semester")  # Submitted semester lina

            if department_id:
                level = self.get_department_level(department_id)  # Department ko level nikalne

                if level:
                    self.initial["level"] = level.pk  # Level automatically set garne

                semesters = self.department_semester_map.get(str(department_id), [])  # Department ko available semesters lina
                self.fields["semester"].choices = [("", "Select Semester")] + [(semester_value, f"Semester {semester_value}") for semester_value in semesters]  # Semester choices set garne

                if semester:
                    self.fields["subject"].queryset = self.get_teacher_subjects(department_id, semester)  # Matching subjects dekhaune

        elif self.instance.pk:
            department_id = self.instance.department_id  # Existing task ko department lina

            if department_id:
                level = self.get_department_level(department_id)  # Department ko level nikalne

                if level:
                    self.initial["level"] = level.pk  # Level automatically set garne

                semesters = self.department_semester_map.get(str(department_id), [])  # Existing department ko semesters lina
                self.fields["semester"].choices = [("", "Select Semester")] + [(semester_value, f"Semester {semester_value}") for semester_value in semesters]  # Semester choices set garne
                self.fields["subject"].queryset = self.get_teacher_subjects(department_id, self.instance.semester)  # Existing task ko subjects dekhaune

    def clean_show_at(self):
        show_at = self.cleaned_data.get("show_at")  # Form bata show time lina

        if not show_at:
            return show_at

        kathmandu = ZoneInfo("Asia/Kathmandu")  # Kathmandu timezone set garne

        if show_at.tzinfo is None:
            show_at = show_at.replace(tzinfo=kathmandu)  # Timezone add garne

        return show_at

    def clean_due_date(self):
        due_date = self.cleaned_data.get("due_date")  # Form bata due date lina

        if not due_date:
            return due_date

        kathmandu = ZoneInfo("Asia/Kathmandu")  # Kathmandu timezone set garne

        if due_date.tzinfo is None:
            due_date = due_date.replace(tzinfo=kathmandu)  # Timezone add garne

        return due_date

    def get_teacher_subjects(self, department_id, semester):
        if not self.teacher or not department_id or not semester:
            return Subject.objects.none()  # Required data nabhaye empty queryset return garne

        try:
            semester = int(semester)  # Semester lai integer ma convert garne
        except (TypeError, ValueError):
            return Subject.objects.none()  # Invalid semester bhaye empty queryset return garne

        subject_ids = TeacherAssignment.objects.filter(teacher=self.teacher, subject__department_id=department_id, semester=semester).values_list("subject_id", flat=True).distinct()  # Teacher ko matching subject IDs nikalne

        return Subject.objects.filter(id__in=subject_ids, department_id=department_id, semester=semester).select_related("level", "department").order_by("name")  # Matching subjects return garne

    def get_department_level(self, department_id):
        try:
            department_id = int(department_id)  # Department ID integer ma convert garne
        except (TypeError, ValueError):
            return None  # Invalid ID bhaye None return garne

        levels = Level.objects.filter(subjects__department_id=department_id).distinct().order_by("name")  # Department sanga related levels nikalne

        if levels.count() == 1:
            return levels.first()  # Euta level matra bhaye return garne

        return None  # Unique level nabhaye None return garne

    def clean(self):
        cleaned_data = super().clean()  # Parent form ko validation run garne

        department = cleaned_data.get("department")  # Selected department lina
        semester = cleaned_data.get("semester")  # Selected semester lina
        subject = cleaned_data.get("subject")  # Selected subject lina
        level = None  # Level ko initial value

        if department:
            level = self.get_department_level(department.id)  # Department ko unique level nikalne

            if not level:
                raise ValidationError({"department": "This department does not have one unique level assigned through its subjects."})  # Unique level nabhaye error

            cleaned_data["level"] = level  # Level cleaned data ma set garne

        if department and semester:
            try:
                semester = int(semester)  # Semester integer ma convert garne
            except (TypeError, ValueError):
                raise ValidationError({"semester": "Invalid semester selected."})  # Invalid semester ko error

            if not self.get_teacher_subjects(department.id, semester).exists():
                raise ValidationError({"semester": "You have no subject assigned for this department and semester."})  # Teacher ko subject nabhaye error

        if subject and department and semester:
            if subject.department_id != department.id:
                raise ValidationError({"subject": "Selected subject does not belong to the selected department."})  # Department mismatch ko error

            if subject.semester != int(semester):
                raise ValidationError({"subject": "Selected subject does not belong to the selected semester."})  # Semester mismatch ko error

            if level and subject.level_id != level.id:
                raise ValidationError({"subject": "Selected subject does not belong to the selected level."})  # Level mismatch ko error

            if self.teacher and not TeacherAssignment.objects.filter(teacher=self.teacher, subject__department_id=department.id, semester=int(semester), subject_id=subject.id).exists():
                raise ValidationError({"subject": "You are not assigned to teach this subject for the selected department and semester."})  # Teacher assignment check garne

        return cleaned_data  # Validated data return garne

    def save(self, commit=True):
        instance = super().save(commit=False)  # Save nagari instance banaune
        department = self.cleaned_data.get("department")  # Selected department lina

        if department:
            instance.level = self.get_department_level(department.id)  # Level automatically set garne

        if commit:
            instance.save()  # Database ma save garne

        return instance  # Instance return garne


class AssignmentSubmissionForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ["file"]  # File field matra rakhne

        widgets = {
            "file": forms.ClearableFileInput(attrs={"class": "form-control", "accept": ".pdf,.doc,.docx"}),  # File upload ko input
        }

    def clean_file(self):
        uploaded_file = self.cleaned_data.get("file")  # Uploaded file lina

        if not uploaded_file:
            raise ValidationError("Please select an assignment file.")  # File nabhaye error

        allowed_extensions = (".pdf", ".doc", ".docx")  # Allowed file extensions

        if not uploaded_file.name.lower().endswith(allowed_extensions):
            raise ValidationError("Only PDF, DOC and DOCX files are allowed.")  # Wrong file type bhaye error

        max_size = 10 * 1024 * 1024  # Maximum 10 MB size

        if uploaded_file.size > max_size:
            raise ValidationError("Maximum file size is 10 MB.")  # File thulo bhaye error

        return uploaded_file  # Valid file return garne