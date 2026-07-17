from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from assignments.models import Assignment


@login_required
def student_dashboard(request):

    if request.user.role != "student":
        return redirect("login")

    assignments = Assignment.objects.filter(
        student=request.user
    ).order_by("-submitted_at")

    accepted_count = assignments.filter(
        status="accepted"
    ).count()

    rejected_count = assignments.filter(
        status="rejected"
    ).count()

    pending_count = assignments.filter(
        status="pending"
    ).count()

    context = {
        "assignments": assignments,
        "accepted_count": accepted_count,
        "rejected_count": rejected_count,
        "pending_count": pending_count,
    }

    return render(
        request,
        "student_dashboard.html",
        context,
    )


@login_required
def teacher_dashboard(request):

    if request.user.role != "teacher":
        return redirect("login")

    assignments = Assignment.objects.filter(
        teacher=request.user
    ).order_by("-submitted_at")

    accepted_count = assignments.filter(
        status="accepted"
    ).count()

    rejected_count = assignments.filter(
        status="rejected"
    ).count()

    pending_count = assignments.filter(
        status="pending"
    ).count()

    context = {
        "assignments": assignments,
        "accepted_count": accepted_count,
        "rejected_count": rejected_count,
        "pending_count": pending_count,
    }

    return render(
        request,
        "teacher_dashboard.html",
        context,
    )