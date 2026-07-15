from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render


@login_required
def student_dashboard(request):

    if request.user.role != 'student':
        return redirect('login')

    return render(
        request,
        'dashboard/student_dashboard.html'
    )


@login_required
def teacher_dashboard(request):

    if request.user.role != 'teacher':
        return redirect('login')

    return render(
        request,
        'dashboard/teacher_dashboard.html'
    )