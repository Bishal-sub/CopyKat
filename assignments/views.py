import os
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from similarity.services import analyze_assignment, get_text_from_file, find_matching_sentences

from .forms import AssignmentSubmissionForm, TeacherTaskForm
from .models import Assignment, TeacherTask


@login_required
def give_assignment(request):
    if request.user.role != "teacher":
        return redirect("login")

    if request.method == "POST":
        form = TeacherTaskForm(request.POST, teacher=request.user)

        if form.is_valid():
            task = form.save(commit=False)
            task.teacher = request.user
            task.save()
            messages.success(request, "Assignment scheduled successfully.")
            return redirect("teacher_dashboard")
    else:
        form = TeacherTaskForm(teacher=request.user)

    return render(request, "give_assignment.html", {"form": form})


@login_required
def view_assignments(request):
    if request.user.role != "student":
        return redirect("login")

    now = timezone.now()

    tasks = TeacherTask.objects.filter(
        batch=request.user.admission_year,
        department_id=request.user.department_id,
        level_id=request.user.level_id,
        show_at__lte=now
    ).select_related(
        "teacher", "subject", "level", "department"
    ).order_by("-show_at")

    task_data = []

    for task in tasks:
        submission = Assignment.objects.filter(task=task, student=request.user).first()

        if submission and submission.status in ("accepted", "final_rejected"):
            continue

        task_data.append({"task": task, "assignment": submission})

    return render(request, "view_assignments.html", {"tasks": task_data})


@login_required
def submit_assignment(request, task_id):
    if request.user.role != "student":
        return redirect("login")

    task = get_object_or_404(
        TeacherTask.objects.select_related("teacher", "subject", "level", "department"),
        id=task_id
    )

    if task.batch != request.user.admission_year or task.department_id != request.user.department_id or task.level_id != request.user.level_id:
        messages.error(request, "This assignment is not assigned to you.")
        return redirect("view_assignments")

    now = timezone.now()

    if now < task.show_at:
        messages.error(request, "This assignment is not available yet.")
        return redirect("view_assignments")

    if now > task.due_date:
        messages.error(request, "Assignment due date has passed.")
        return redirect("view_assignments")

    existing_submission = Assignment.objects.filter(task=task, student=request.user).first()

    if existing_submission:
        messages.error(request, "You have already submitted this assignment.")
        return redirect("view_assignments")

    if request.method == "POST":
        form = AssignmentSubmissionForm(request.POST, request.FILES)

        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.task = task
            assignment.student = request.user
            assignment.teacher = task.teacher
            assignment.subject = task.subject
            assignment.title = task.topic
            assignment.semester = task.semester
            assignment.level = task.level
            assignment.department = task.department
            assignment.status = "pending_review"
            assignment.submission_attempt = 1
            assignment.resubmission_used = False
            assignment.resubmission_deadline = None
            assignment.teacher_remark = ""
            assignment.reviewed_at = None
            assignment.similarity_percentage = "0%"
            assignment.matched_assignment = None
            assignment.matching_text = ""
            assignment.save()

            analyze_assignment(assignment)

            assignment.refresh_from_db()

            if assignment.matched_assignment and assignment.matched_assignment.student_id == assignment.student_id:
                assignment.matched_assignment = None
                assignment.similarity_percentage = "0%"
                assignment.matching_text = ""
                assignment.save(update_fields=["matched_assignment", "similarity_percentage", "matching_text"])

            messages.success(request, "Assignment submitted successfully.")
            return redirect("view_assignments")
    else:
        form = AssignmentSubmissionForm()

    return render(request, "submit_assignment.html", {"form": form, "task": task})


@login_required
def resubmit_assignment(request, assignment_id):
    if request.user.role != "student":
        return redirect("login")

    assignment = get_object_or_404(
        Assignment.objects.select_related("task", "teacher", "subject", "level", "department"),
        id=assignment_id,
        student=request.user,
        status="resubmission_required"
    )

    if not assignment.task:
        messages.error(request, "This assignment is no longer available.")
        return redirect("view_assignments")

    if assignment.submission_attempt != 1:
        messages.error(request, "This assignment cannot be resubmitted.")
        return redirect("view_assignments")

    if assignment.resubmission_used:
        messages.error(request, "Resubmission already used.")
        return redirect("view_assignments")

    if assignment.task.batch != request.user.admission_year or assignment.task.department_id != request.user.department_id or assignment.task.level_id != request.user.level_id:
        messages.error(request, "This assignment is not assigned to you.")
        return redirect("view_assignments")

    now = timezone.now()

    if now > assignment.task.due_date:
        messages.error(request, "Assignment due date has passed.")
        return redirect("view_assignments")

    if assignment.resubmission_deadline and now > assignment.resubmission_deadline:
        messages.error(request, "Resubmission deadline has passed.")
        return redirect("view_assignments")

    if request.method == "POST":
        new_file = request.FILES.get("file")

        if not new_file:
            messages.error(request, "Please select a file.")
            return redirect("resubmit_assignment", assignment_id=assignment.id)

        if not new_file.name.lower().endswith((".pdf", ".doc", ".docx")):
            messages.error(request, "Only PDF, DOC and DOCX files are allowed.")
            return redirect("resubmit_assignment", assignment_id=assignment.id)

        if new_file.size > 10 * 1024 * 1024:
            messages.error(request, "Maximum file size is 10 MB.")
            return redirect("resubmit_assignment", assignment_id=assignment.id)

        old_file_path = None

        if assignment.file:
            try:
                old_file_path = assignment.file.path
            except (ValueError, FileNotFoundError):
                old_file_path = None

        assignment.file = new_file
        assignment.status = "pending_review"
        assignment.teacher_remark = ""
        assignment.reviewed_at = None
        assignment.similarity_percentage = "0%"
        assignment.matched_assignment = None
        assignment.matching_text = ""
        assignment.resubmission_used = True
        assignment.resubmission_deadline = None
        assignment.submission_attempt = 2
        assignment.save()

        if old_file_path and os.path.exists(old_file_path):
            try:
                os.remove(old_file_path)
            except OSError:
                pass

        analyze_assignment(assignment)

        assignment.refresh_from_db()

        if assignment.matched_assignment and assignment.matched_assignment.student_id == assignment.student_id:
            assignment.matched_assignment = None
            assignment.similarity_percentage = "0%"
            assignment.matching_text = ""
            assignment.save(update_fields=["matched_assignment", "similarity_percentage", "matching_text"])

        messages.success(request, "Assignment resubmitted successfully.")
        return redirect("view_assignments")

    return render(request, "resubmit_assignment.html", {"assignment": assignment})


@login_required
def teacher_review(request, id):
    if request.user.role != "teacher":
        return redirect("login")

    assignment = get_object_or_404(
        Assignment.objects.select_related(
            "student",
            "teacher",
            "subject",
            "level",
            "department",
            "task",
            "matched_assignment",
            "matched_assignment__student",
        ),
        id=id,
        teacher=request.user,
    )

    if request.method == "POST":
        status = request.POST.get("status")
        assignment.teacher_remark = request.POST.get("remark", "").strip()

        if status == "accepted":
            assignment.status = "accepted"
            assignment.resubmission_deadline = None

        elif status == "resubmission_required":
            if assignment.submission_attempt != 1:
                messages.error(request, "A second submission cannot be rejected for another resubmission.")
                return redirect("teacher_dashboard")

            if assignment.resubmission_used:
                messages.error(request, "Resubmission has already been used.")
                return redirect("teacher_dashboard")

            assignment.status = "resubmission_required"
            assignment.resubmission_deadline = timezone.now() + timedelta(days=2)

            if assignment.task and assignment.resubmission_deadline > assignment.task.due_date:
                assignment.resubmission_deadline = assignment.task.due_date

        elif status == "final_rejected":
            assignment.status = "final_rejected"
            assignment.resubmission_deadline = None

        elif status == "pending_review":
            assignment.status = "pending_review"

        else:
            messages.error(request, "Invalid review status.")
            return redirect("teacher_dashboard")

        assignment.reviewed_at = timezone.now()
        assignment.save()

        messages.success(request, "Assignment reviewed successfully.")
        return redirect("teacher_dashboard")

    matching_sentences = []
    document_text = ""

    # Current assignment ko original/raw text UI ko display garna nikalne
    try:
        document_text = get_text_from_file(assignment.file.path)
    except Exception:
        document_text = ""

    # Different student ko assignment sanga matra matching content check garne
    if assignment.matched_assignment and assignment.matched_assignment.student_id != assignment.student_id:
        try:
            # Similarity ko lagi clean text use garne hoina, matching ko lagi raw text use garne
            current_text = get_text_from_file(assignment.file.path)
            old_text = get_text_from_file(assignment.matched_assignment.file.path)

            # Raw text use gareko le original capital letter, punctuation ra position preserve huncha
            matching_sentences = find_matching_sentences(current_text, old_text)
        except Exception:
            matching_sentences = []

    return render(
        request,
        "teacher_review.html",
        {
            "assignment": assignment,
            "document_text": document_text,
            "matching_sentences": matching_sentences,
        },
    )