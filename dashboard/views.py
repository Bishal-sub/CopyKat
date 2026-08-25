from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone


from assignments.models import Assignment, TeacherTask


# Student ko dashboard ma afno batch ko tasks ra submission status dekhau na
@login_required
def student_dashboard(request):

    # Student matra student dashboard access garna paos
    if request.user.role != "student":
        return redirect("login")

    # Ahile ko current date ra time 
    now = timezone.now()

    # Student ko batch, level ra department sanga match hune ra schedule time aaipugeko tasks matra 
    all_tasks = TeacherTask.objects.filter(batch=request.user.admission_year, level=request.user.level, department=request.user.department, show_at__lte=now).select_related("teacher", "subject", "level", "department")

    # Student le submit gareko assignments ko details 
    assignments = Assignment.objects.filter(student=request.user).select_related("task", "subject", "teacher")

    tasks = []

    # Student ko lagi active tasks haru check garne
    for task in all_tasks:

        # Yo task ko lagi student le pahile nai assignment submit gareko cha ki chaina
        submission = Assignment.objects.filter(task=task, student=request.user).first()

        # Assignment accepted wa final rejected bhayepachi "Assignments To Do" ma feri count nagarne
        if submission and submission.status in ["accepted", "final_rejected"]:
            continue

        # Active task list ma task add garne
        tasks.append(task)

    # Student dashboard ma dekhine total active tasks ko count
    total_tasks = len(tasks)

    # Student le submit gareko total assignments ko count
    submitted_count = assignments.count()

    # Teacher le review garna baki assignments ko count
    pending_count = assignments.filter(status="pending_review").count()

    # Final rejected bhayeko assignments ko count
    rejected_count = assignments.filter(status="final_rejected").count()

    # Dashboard template lai sabai required data pathaune
    context = {
        "tasks": tasks,
        "assignments": assignments,
        "total_tasks": total_tasks,
        "submitted_count": submitted_count,
        "pending_count": pending_count,
        "rejected_count": rejected_count,
    }

    return render(request, "student_dashboard.html", context)



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