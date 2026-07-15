from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from .forms import StudentRegisterForm


def register_view(request):

    if request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':

        form = StudentRegisterForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            user = form.save(commit=False)
            user.role = 'student'
            user.save()

            return redirect('login')

    else:
        form = StudentRegisterForm()

    return render(
        request,
        'register.html',
        {'form': form}
    )


def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            if user.is_superuser:
                return redirect('/admin/')

            if user.role == 'teacher':
                return redirect('teacher_dashboard')

            return redirect('student_dashboard')

    return render(request, 'login.html')


def logout_view(request):

    logout(request)

    return redirect('login')