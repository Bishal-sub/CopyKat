from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path("verify-email/",views.verify_email,name="verify_email",),
    path("forgot-password/",views.forgot_password_view,name="forgot_password"),
    path("verify-reset-otp/",views.verify_reset_otp_view,name="verify_reset_otp"),
    path("reset-password/",views.reset_password_view,name="reset_password"),
    path("teacher-change-password/",views.teacher_change_password,name="teacher_change_password"),
]