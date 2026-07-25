from django.urls import path
from . import views

urlpatterns = [

    path(
        "",
        views.similarity_home,
        name="similarity_home",
    ),

]