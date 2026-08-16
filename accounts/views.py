from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import User, EmailVerificationOTP, PasswordResetOTP
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
            EmailVerificationOTP.objects.create(user=user, otp=otp)

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

    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect("/admin/")

        if request.user.role == "teacher":
            if request.user.first_login:
                request.session["force_password_user"] = request.user.id
                return redirect("teacher_change_password")

            return redirect("teacher_dashboard")

        return redirect("student_dashboard")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            account = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, "Invalid username or password.")
            return render(request, "login.html")

        if not account.is_active:
            if account.check_password(password):
                otp = str(random.randint(100000, 999999))
                EmailVerificationOTP.objects.filter(user=account).delete()
                EmailVerificationOTP.objects.create(user=account, otp=otp)

                send_mail(
                    "CopyKat Email Verification",
                    f"Your verification code is: {otp}",
                    settings.EMAIL_HOST_USER,
                    [account.email],
                    fail_silently=False,
                )

                request.session["verification_user_id"] = account.id
                return redirect("verify_email")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            if user.is_superuser:
                return redirect("/admin/")

            if user.role == "teacher":
                if user.first_login:
                    request.session["force_password_user"] = user.id
                    return redirect("teacher_change_password")

                return redirect("teacher_dashboard")

            return redirect("student_dashboard")

        messages.error(request, "Invalid username or password.")

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
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
            return render(request, "verify_email.html", {"error": "OTP not found."})

        if otp_record.is_expired():
            return render(request, "verify_email.html", {"error": "OTP expired."})

        if entered_otp == otp_record.otp:
            user.is_active = True
            user.save()
            otp_record.delete()

            request.session.pop("verification_user_id", None)
            messages.success(request, "Email verified successfully. You can now login.")
            return redirect("login")

        return render(request, "verify_email.html", {"error": "Invalid OTP."})

    return render(request, "verify_email.html")


def forgot_password_view(request):
    if request.method == "POST":
        username = request.POST.get("username")

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, "Username not found.")
            return redirect("forgot_password")

        otp = str(random.randint(100000, 999999))
        PasswordResetOTP.objects.filter(user=user).delete()
        PasswordResetOTP.objects.create(user=user, otp=otp)

        send_mail(
            "CopyKat Password Reset",
            f"Your OTP is: {otp}",
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )

        request.session["reset_user_id"] = user.id
        return redirect("verify_reset_otp")

    return render(request, "forgot_password.html")


def verify_reset_otp_view(request):
    user_id = request.session.get("reset_user_id")

    if not user_id:
        return redirect("forgot_password")

    user = User.objects.get(id=user_id)

    if request.method == "POST":
        entered_otp = request.POST.get("otp")

        otp_obj = (
            PasswordResetOTP.objects
            .filter(user=user)
            .order_by("-created_at")
            .first()
        )

        if not otp_obj:
            messages.error(request, "OTP not found.")
            return redirect("verify_reset_otp")

        if otp_obj.is_expired():
            messages.error(request, "OTP expired.")
            return redirect("verify_reset_otp")

        if entered_otp != otp_obj.otp:
            messages.error(request, "Invalid OTP.")
            return redirect("verify_reset_otp")

        return redirect("reset_password")

    return render(request, "verify_reset_otp.html")


def reset_password_view(request):
    user_id = request.session.get("reset_user_id")

    if not user_id:
        return redirect("forgot_password")

    user = User.objects.get(id=user_id)

    if request.method == "POST":
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("reset_password")

        user.set_password(password1)
        user.save()

        PasswordResetOTP.objects.filter(user=user).delete()
        del request.session["reset_user_id"]

        messages.success(request, "Password updated successfully.")
        return redirect("login")

    return render(request, "reset_password.html")


def teacher_change_password(request):
    user_id = request.session.get("force_password_user")

    if not user_id:
        return redirect("login")

    user = User.objects.get(id=user_id)

    if request.method == "POST":
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("teacher_change_password")

        user.set_password(password1)
        user.first_login = False
        user.save()

        del request.session["force_password_user"]
        messages.success(request, "Password changed successfully.")

        return redirect("login")

    return render(request, "teacher_change_password.html")