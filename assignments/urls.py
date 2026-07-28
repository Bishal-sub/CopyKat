from django.urls import path
from . import views

urlpatterns = [

    path(
        "submit/",
        views.submit_assignment,
        name="submit_assignment",
    ),

    path(
        "resubmit/<int:assignment_id>/",
        views.resubmit_assignment,
        name="resubmit_assignment",
    ),

    path(
        "review/<int:id>/",
        views.teacher_review,
        name="teacher_review",
    ),

    path(
        "subject-details/<int:subject_id>/",
        views.subject_details,
        name="subject_details",
    ),

]