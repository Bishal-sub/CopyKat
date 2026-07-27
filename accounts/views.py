from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .forms import StudentRegisterForm


def register_view(request):
    if request.user.is_authenticated:
        return redirect("login")

    if request.method == "POST":
        form = StudentRegisterForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save(commit=False)
            user.role = "student"
            user.save()
            return redirect("login")
        else:
            print(form.errors)
    else:
        form = StudentRegisterForm()

    return render(
        request,
        "register.html",
        {
            "form": form,
        },
    )


def login_view(request):

    if request.user.is_authenticated:

        if request.user.is_superuser:
            return redirect("/admin/")

        elif request.user.role == "teacher":
            return redirect("teacher_dashboard")

        elif request.user.role == "student":
            return redirect("student_dashboard")

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is not None:

            login(request, user)

            if user.is_superuser:
                return redirect("/admin/")

            elif user.role == "teacher":
                return redirect("teacher_dashboard")

            return redirect("student_dashboard")

        else:

            messages.error(
                request,
                "Invalid username or password."
            )

    return render(
        request,
        "login.html"
    )

def logout_view(request):
    logout(request)
    return redirect("login")