from datetime import datetime, date
from uuid import UUID

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from .application_services import (
    ScreeningApplicationService,
    RecruiterApplicationService,
)


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "recruitment/index.html")


def show_screenings(request: HttpRequest) -> HttpResponse:
    screening_application_service = ScreeningApplicationService()
    screenings = screening_application_service.get_all_screenings()
    context = {"screenings": screenings}
    return render(request, "recruitment/screenings.html", context=context)


def show_screening(request: HttpRequest, id: UUID) -> HttpResponse:
    screening_application_service = ScreeningApplicationService()
    screening = screening_application_service.get_screening(id)
    context = {"screening": screening}
    return render(request, "recruitment/screening.html", context=context)


def add_next_interview_screening(request: HttpRequest, id: UUID) -> HttpResponse:
    screening_application_service = ScreeningApplicationService()
    recruiter_application_service = RecruiterApplicationService()
    if request.method == "GET":
        screening = screening_application_service.get_screening(id)
        recruiters = recruiter_application_service.get_all_recruiters()
        context = {"screening": screening, "recruiters": recruiters}
        return render(
            request, "recruitment/add_next_interview_screening.html", context=context
        )
    elif request.method == "POST":
        interview_date_str: str = request.POST["interview_date"]
        tdatetime = datetime.strptime(interview_date_str, "%Y-%m-%d")
        interview_date: date = date(tdatetime.year, tdatetime.month, tdatetime.day)
        recruiter_id: str = request.POST["recruiter_id"]
        screening_application_service.add_next_interview(
            screening_id=id,
            interview_date=interview_date,
            recruiter_id=UUID(recruiter_id),
        )
        return redirect("recruitment:show_screening", id=id)
    raise Exception("想定外のHTTPリクエストメソッドです。")


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


def start_from_pre_interview_screening(request: HttpRequest) -> HttpResponse:
    screening_application_service = ScreeningApplicationService()
    if request.method == "GET":
        return render(request, "recruitment/start_from_pre_interview_screening.html")
    elif request.method == "POST":
        applicant_email_address = request.POST.get("applicant_email_address")
        screening_application_service.start_from_pre_interview(
            applicant_email_address=applicant_email_address
        )
        return redirect("recruitment:show_screenings")
    raise Exception("想定外のHTTPリクエストメソッドです。")
