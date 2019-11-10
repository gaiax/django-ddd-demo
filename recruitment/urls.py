from django.urls import path

from . import views

app_name = "recruitment"
urlpatterns = [
    path("", views.index),
    path("screenings/", views.show_screenings, name="show_screenings"),
    path("screenings/<uuid:id>", views.show_screening, name="show_screening"),
    path(
        "screenings/<uuid:id>/add_next_interview",
        views.add_next_interview_screening,
        name="add_next_interview_screening",
    ),
    path("screenings/apply", views.apply_screening, name="apply_screening"),
    path(
        "screenings/start_from_pre_interview",
        views.start_from_pre_interview_screening,
        name="start_from_pre_interview_screening",
    ),
]
