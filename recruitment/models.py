from uuid import uuid4

from django.db import models


class RecruiterRDB(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class ScreeningRDB(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    apply_date = models.DateField()
    status = models.SmallIntegerField()
    applicant_email_address = models.EmailField()

    def __str__(self) -> str:
        return self.applicant_email_address


class InterviewRDB(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    screening = models.ForeignKey(ScreeningRDB, on_delete=models.CASCADE)
    interview_date = models.DateField()
    interview_number = models.IntegerField()
    screening_step_result = models.SmallIntegerField()
    recruiter = models.ForeignKey(RecruiterRDB, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.interview_date.strftime("%Y/%m/%d")
