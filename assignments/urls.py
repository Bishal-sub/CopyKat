from django.urls import path

from . import views


urlpatterns = [
    path("give-assignment/",views.give_assignment,name="give_assignment",),
    path("assignments/",views.view_assignments,name="view_assignments",),
    path("submit-assignment/<int:task_id>/",views.submit_assignment,name="submit_assignment",),
    path("resubmit-assignment/<int:assignment_id>/",views.resubmit_assignment,name="resubmit_assignment",),
    path("teacher-review/<int:id>/",views.teacher_review,name="teacher_review",),
]