from django.contrib.auth.decorators import login_required
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)
from django.utils import timezone

import os

from accounts.models import User
from .models import Assignment

from similarity.services import ( analyze_assignment )



# SUBMIT ASSIGNMENT


@login_required
def submit_assignment(request):

    if request.user.role != "student":
        return redirect("login")

    teachers = User.objects.filter(
        role="teacher"
    )

    if request.method == "POST":

        assignment = Assignment.objects.create(

            student=request.user,

            title=request.POST.get(
                "title"
            ),

            teacher_id=request.POST.get(
                "teacher"
            ),

            level=request.POST.get(
                "level"
            ),

            semester=request.POST.get(
                "semester"
            ),

            file=request.FILES.get(
                "file"
            ),

        )

        # Calculate similarity
        analyze_assignment(
            assignment
        )

        return redirect(
            "student_dashboard"
        )

    return render(
        request,
        "submit_assignment.html",
        {
            "teachers": teachers
        }
    )



# RESUBMIT ASSIGNMENT


@login_required
def resubmit_assignment(
    request,
    assignment_id
):

    if request.user.role != "student":
        return redirect("login")

    assignment = get_object_or_404(

        Assignment,

        id=assignment_id,

        student=request.user,

        status="rejected",

    )

    if request.method == "POST":

        new_file = request.FILES.get(
            "file"
        )

        if new_file:

            # Delete old file
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

            # Replace old file
            assignment.file = new_file

            # Reset review information
            assignment.status = "pending"

            assignment.teacher_remark = ""

            assignment.reviewed_at = None

            assignment.similarity_percentage = 0

            assignment.save()

            # Recalculate similarity
            analyze_assignment(
                assignment
            )

        return redirect(
            "student_dashboard"
        )

    return render(
        request,
        "resubmit_assignment.html",
        {
            "assignment": assignment,
        }
    )



# TEACHER REVIEW


@login_required
def teacher_review(
    request,
    id
):

    if request.user.role != "teacher":
        return redirect("login")

    assignment = get_object_or_404(

        Assignment,

        id=id,

        teacher=request.user,

    )

    if request.method == "POST":

        assignment.teacher_remark = request.POST.get(
            "remark"
        )

        assignment.status = request.POST.get(
            "status"
        )

        assignment.reviewed_at = timezone.now()

        assignment.save()

        return redirect(
            "teacher_dashboard"
        )

    return render(
        request,
        "teacher_review.html",
        {
            "assignment": assignment
        }
    )