from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from assignments.models import Assignment, TeacherTask


# Student ko dashboard ma afno batch ko tasks ra submission status dekhau na
@login_required
def student_dashboard(request):

    # Student matra student dashboard access garna paos
    if request.user.role != "student":
        return redirect("login")

    # Student ko batch ko tasks matra retrieve garne
    all_tasks = TeacherTask.objects.filter(
        batch=request.user.admission_year
    ).select_related("teacher", "subject")

    # Student le submit gareko assignments ko details retrieve garne
    assignments = Assignment.objects.filter(
        student=request.user
    ).select_related("task", "subject", "teacher")

    tasks = []

    # Accepted ra Final Rejected assignment task count ma nadekhaune
    for task in all_tasks:

        submission = Assignment.objects.filter(
            task=task,
            student=request.user
        ).first()

        # Accepted ra Final Rejected assignment lai active task namanne
        if submission and submission.status in ["accepted", "final_rejected"]:
            continue

        tasks.append(task)

    # Dashboard ma active task ko total count dekhau na
    total_tasks = len(tasks)

    # Student le submit gareko assignment ko total count
    submitted_count = assignments.count()

    # Teacher review garna baki assignments ko count
    pending_count = assignments.filter(
        status="pending_review"
    ).count()

    # Final rejected assignments ko count
    rejected_count = assignments.filter(
        status="final_rejected"
    ).count()

    # Dashboard template lai required data ekai thau bata pathauna
    context = {
        "tasks": tasks,
        "assignments": assignments,
        "total_tasks": total_tasks,
        "submitted_count": submitted_count,
        "pending_count": pending_count,
        "rejected_count": rejected_count,
    }

    return render(
        request,
        "student_dashboard.html",
        context
    )


# Teacher ko dashboard ma tasks ra student submissions ko summary dekhau na
@login_required
def teacher_dashboard(request):

    # Teacher matra teacher dashboard access garna paos
    if request.user.role != "teacher":
        return redirect("login")

    # Teacher ko submissions latest first ma dekhau na
    assignments = Assignment.objects.filter(
        teacher=request.user
    ).order_by("-submitted_at")

    # Teacher le create gareko tasks latest first ma dekhau na
    tasks = TeacherTask.objects.filter(
        teacher=request.user
    ).order_by("-created_at")

    # Teacher le create gareko total tasks count
    total_tasks = tasks.count()

    # Accepted submissions ko count
    accepted_count = assignments.filter(
        status="accepted"
    ).count()

    # Final rejected submissions ko count
    rejected_count = assignments.filter(
        status="final_rejected"
    ).count()

    # Teacher le review garnu baki submissions ko count
    pending_count = assignments.filter(
        status="pending_review"
    ).count()

    # Dashboard template lai summary ra records pathauna
    context = {
        "assignments": assignments,
        "tasks": tasks,
        "total_tasks": total_tasks,
        "accepted_count": accepted_count,
        "rejected_count": rejected_count,
        "pending_count": pending_count,
    }

    return render(
        request,
        "teacher_dashboard.html",
        context
    )