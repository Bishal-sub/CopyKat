from django.urls import path
from . import views



urlpatterns = [


    path(

        "submit/",

        views.submit_assignment,

        name="submit_assignment"

    ),



    path(

        "review/<int:id>/",

        views.teacher_review,

        name="teacher_review"

    ),


]