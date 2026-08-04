from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

from .models import User, EmailVerificationOTP
from .forms import StudentRegisterForm

import random


def register_view(request):

    if request.user.is_authenticated:
        return redirect("login")

    if request.method == "POST":

        form = StudentRegisterForm(request.POST, request.FILES)

        if form.is_valid():

            user = form.save(commit=False)

            user.role = "student"
            user.is_active = False

            user.save()

            otp = str(random.randint(100000, 999999))

            EmailVerificationOTP.objects.create(
                user=user,
                otp=otp
            )

            send_mail(
                "CopyKat Email Verification",
                f"Your verification code is: {otp}",
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )

            request.session["verification_user_id"] = user.id

            

            return redirect("verify_email")

    else:

        form = StudentRegisterForm()

    return render(
        request,
        "register.html",
        {"form": form}
    )

def login_view(request):

    if request.user.is_authenticated:

        if request.user.is_superuser:
            return redirect("/admin/")

        if request.user.role == "teacher":
            return redirect("teacher_dashboard")

        return redirect("student_dashboard")

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            account = User.objects.get(username=username)

        except User.DoesNotExist:

            messages.error(
                request,
                "Invalid username or password."
            )

            return render(request, "login.html")

        if not account.is_active:

            if account.check_password(password):

                otp = str(random.randint(100000, 999999))

                EmailVerificationOTP.objects.create(
                    user=account,
                    otp=otp
                )

                send_mail(
                    "CopyKat Email Verification",
                    f"Your verification code is: {otp}",
                    settings.EMAIL_HOST_USER,
                    [account.email],
                    fail_silently=False,
                )

                request.session["verification_user_id"] = account.id

                

                return redirect("verify_email")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:

            login(request, user)

            if user.is_superuser:
                return redirect("/admin/")

            if user.role == "teacher":
                return redirect("teacher_dashboard")

            return redirect("student_dashboard")

        messages.error(
            request,
            "Invalid username or password."
        )

    return render(request, "login.html")


def logout_view(request):

    logout(request)

    messages.success(
        request,
        "You have been logged out successfully."
    )

    return redirect("login")


def verify_email(request):

    user_id = request.session.get("verification_user_id")

    if not user_id:
        return redirect("register")

    try:
        user = User.objects.get(id=user_id)

    except User.DoesNotExist:
        return redirect("register")

    if request.method == "POST":

        entered_otp = request.POST.get("otp")

        otp_record = (
            EmailVerificationOTP.objects
            .filter(user=user)
            .order_by("-created_at")
            .first()
        )

        if not otp_record:

            return render(
                request,
                "verify_email.html",
                {"error": "OTP not found."}
            )

        if otp_record.is_expired():

            return render(
                request,
                "verify_email.html",
                {"error": "OTP expired."}
            )

        if entered_otp == otp_record.otp:

            user.is_active = True
            user.save()

            otp_record.delete()

            request.session.pop(
                "verification_user_id",
                None
            )

            messages.success(
                request,
                "Email verified successfully. You can now login."
            )

            return redirect("login")

        return render(
            request,
            "verify_email.html",
            {"error": "Invalid OTP."}
        )

    return render(request, "verify_email.html")