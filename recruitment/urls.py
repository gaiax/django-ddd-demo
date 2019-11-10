from django.urls import path

from . import views

app_name = "recruitment"
urlpatterns = [
    path("", views.index),
    path("screenings/", views.show_screenings, name="show_screenings"),
    path("screenings/apply", views.apply_screening, name="apply_screening"),
]
