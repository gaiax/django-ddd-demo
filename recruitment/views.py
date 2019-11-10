from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from .application_services import ScreeningApplicationService


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "recruitment/index.html")


def show_screenings(request: HttpRequest) -> HttpResponse:
    screening_application_service = ScreeningApplicationService()
    screenings = screening_application_service.get_all()
    context = {"screenings": screenings}
    return render(request, "recruitment/screenings.html", context=context)


def apply_screening(request: HttpRequest) -> HttpResponse:
    screening_application_service = ScreeningApplicationService()
    if request.method == "GET":
        return render(request, "recruitment/apply_screening.html")
    elif request.method == "POST":
        applicant_email_address = request.POST.get("applicant_email_address")
        screening_application_service.apply(
            applicant_email_address=applicant_email_address
        )
        return redirect("recruitment:show_screenings")
    raise Exception("想定外のHTTPリクエストメソッドです。")
