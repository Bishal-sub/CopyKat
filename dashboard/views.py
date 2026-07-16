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



    return render(
        request,
        "student_dashboard.html",
        {
            "assignments": assignments
        }
    )







@login_required
def teacher_dashboard(request):

    if request.user.role != "teacher":
        return redirect("login")


    assignments = Assignment.objects.filter(
        teacher=request.user
    ).order_by("-submitted_at")



    return render(
        request,
        "teacher_dashboard.html",
        {
            "assignments": assignments
        }
    )