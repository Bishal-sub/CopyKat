from django.urls import path

from . import views


urlpatterns = [

    # ============================================================
    # TEACHER
    # ============================================================

    # Teacher le assignment create garne
    path(
        "give-assignment/",
        views.give_assignment,
        name="give_assignment",
    ),


    # ============================================================
    # STUDENT
    # ============================================================

    # Student le afno assignments herne
    path(
        "assignments/",
        views.view_assignments,
        name="view_assignments",
    ),

    # Student le assignment submit garne
    path(
        "submit-assignment/<int:task_id>/",
        views.submit_assignment,
        name="submit_assignment",
    ),

    # Student le assignment resubmit garne
    path(
        "resubmit-assignment/<int:assignment_id>/",
        views.resubmit_assignment,
        name="resubmit_assignment",
    ),


    # ============================================================
    # TEACHER REVIEW
    # ============================================================

    # Teacher le student ko assignment review garne
    path(
        "teacher-review/<int:id>/",
        views.teacher_review,
        name="teacher_review",
    ),
]