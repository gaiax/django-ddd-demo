from django.contrib import admin

from .models import RecruiterRDB, ScreeningRDB, InterviewRDB


class RecruiterAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]


class ScreeningAdmin(admin.ModelAdmin):
    list_display = ["id", "apply_date", "status", "applicant_email_address"]


class InterviewAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "screening",
        "interview_date",
        "interview_number",
        "screening_step_result",
        "recruiter",
    ]


admin.site.register(RecruiterRDB, RecruiterAdmin)
admin.site.register(ScreeningRDB, ScreeningAdmin)
admin.site.register(InterviewRDB, InterviewAdmin)
