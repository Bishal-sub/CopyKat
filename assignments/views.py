from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)
from django.utils import timezone

import os

from accounts.models import TeacherAssignment

from .models import Assignment
from .forms import AssignmentForm

from similarity.services import analyze_assignment


# ==========================================
# SUBMIT ASSIGNMENT
# ==========================================

@login_required
def submit_assignment(request):

    if request.user.role != "student":
        return redirect("login")

    teacher_assignments = (
        TeacherAssignment.objects.select_related(
            "teacher",
            "subject",
        )
    )

    if request.method == "POST":

        form = AssignmentForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():

            assignment = form.save(
                commit=False
            )

            teacher_assignment = (
                TeacherAssignment.objects.filter(
                    subject=assignment.subject
                ).first()
            )

            if not teacher_assignment:

                form.add_error(
                    None,
                    "No teacher assigned for this subject."
                )

            else:

                assignment.student = request.user

                assignment.teacher = (
                    teacher_assignment.teacher
                )

                assignment.level = (
                    teacher_assignment.level
                )

                assignment.semester = (
                    teacher_assignment.semester
                )

                assignment.save()

                analyze_assignment(
                    assignment
                )

                messages.success(
                    request,
                    "Assignment submitted successfully."
                )

                return redirect(
                    "student_dashboard"
                )

    else:

        form = AssignmentForm()

    return render(
        request,
        "submit_assignment.html",
        {
            "form": form,
            "teacher_assignments": teacher_assignments,
        },
    )


# ==========================================
# RESUBMIT ASSIGNMENT
# ==========================================

@login_required
def resubmit_assignment(
    request,
    assignment_id,
):

    if request.user.role != "student":
        return redirect("login")

    assignment = get_object_or_404(
        Assignment,
        id=assignment_id,
        student=request.user,
        status="rejected",
    )

    if assignment.resubmission_used:

        messages.error(
            request,
            "You have already used your one resubmission."
        )

        return redirect(
            "student_dashboard"
        )

    if request.method == "POST":

        new_file = request.FILES.get(
            "file"
        )

        if not new_file:

            messages.error(
                request,
                "Please select a file."
            )

            return redirect(
                "resubmit_assignment",
                assignment_id=assignment.id,
            )

        allowed_extensions = (
            ".pdf",
            ".doc",
            ".docx",
        )

        if not new_file.name.lower().endswith(
            allowed_extensions
        ):

            messages.error(
                request,
                "Only PDF, DOC and DOCX files are allowed."
            )

            return redirect(
                "resubmit_assignment",
                assignment_id=assignment.id,
            )

        max_size = (
            10 * 1024 * 1024
        )

        if new_file.size > max_size:

            messages.error(
                request,
                "Maximum file size is 10 MB."
            )

            return redirect(
                "resubmit_assignment",
                assignment_id=assignment.id,
            )

        if assignment.file:

            old_file_path = (
                assignment.file.path
            )

            if os.path.exists(
                old_file_path
            ):
                os.remove(
                    old_file_path
                )

        assignment.file = new_file

        assignment.status = "pending"

        assignment.teacher_remark = ""

        assignment.reviewed_at = None

        assignment.similarity_percentage = 0

        assignment.matched_assignment = None

        assignment.resubmission_used = True

        assignment.save()

        analyze_assignment(
            assignment
        )

        messages.success(
            request,
            "Assignment resubmitted successfully."
        )

        return redirect(
            "student_dashboard"
        )

    return render(
        request,
        "resubmit_assignment.html",
        {
            "assignment": assignment,
        },
    )


# ==========================================
# TEACHER REVIEW
# ==========================================

@login_required
def teacher_review(
    request,
    id,
):

    if request.user.role != "teacher":
        return redirect("login")

    assignment = get_object_or_404(
        Assignment,
        id=id,
        teacher=request.user,
    )

    if request.method == "POST":

        assignment.teacher_remark = (
            request.POST.get(
                "remark",
                ""
            )
        )

        assignment.status = (
            request.POST.get(
                "status",
                "pending"
            )
        )

        assignment.reviewed_at = (
            timezone.now()
        )

        assignment.save()

        messages.success(
            request,
            "Assignment reviewed successfully."
        )

        return redirect(
            "teacher_dashboard"
        )

    return render(
        request,
        "teacher_review.html",
        {
            "assignment": assignment,
        },
    )
    
from django.http import JsonResponse
from accounts.models import TeacherAssignment


def subject_details(request, subject_id):

    teacher_assignment = (
        TeacherAssignment.objects.filter(
            subject_id=subject_id
        )
        .select_related(
            "teacher",
            "subject",
        )
        .first()
    )

    if not teacher_assignment:

        return JsonResponse(
            {
                "success": False,
            }
        )

    return JsonResponse(
        {
            "success": True,
            "teacher": teacher_assignment.teacher.full_name,
            "teacher_id": teacher_assignment.teacher.id,
            "semester": teacher_assignment.semester,
            "level": teacher_assignment.level,
        }
    )