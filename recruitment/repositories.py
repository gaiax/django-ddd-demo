from django.db.models.query import QuerySet
from typing import Tuple, List

from .entities import (
    Screening,
    ScreeningId,
    ScreeningStatus,
    Interviews,
    Interview,
    InterviewId,
    ScreeningStepResult,
    RecruiterId,
)
from .models import ScreeningRDB, InterviewRDB, RecruiterRDB


class ScreeningRepository:
    def get(self, screening_id: ScreeningId) -> Screening:
        ...

    def get_all(self) -> List[Screening]:
        screening_rdb_qeury: QuerySet[ScreeningRDB] = ScreeningRDB.objects.all()
        screenings: List[Screening] = []

        screening_rdb: ScreeningRDB
        interview_rdb: InterviewRDB
        for screening_rdb in screening_rdb_qeury:
            interviews: List[Interview] = [
                Interview.reconstruct(
                    interview_id=InterviewId.reconstruct(interview_rdb.id),
                    screening_id=ScreeningId.reconstruct(screening_rdb.id),
                    interview_date=interview_rdb.interview_date,
                    interview_number=interview_rdb.interview_number,
                    screening_step_result=ScreeningStepResult(
                        interview_rdb.screening_step_result
                    ),
                    recruiter_id=RecruiterId.reconstruct(interview_rdb.recruiter.id),
                )
                for interview_rdb in screening_rdb.interviewrdb_set.all()
            ]

            interviews_obj: Interviews = Interviews.reconstruct(
                interviews=interviews,
                screening_id=ScreeningId.reconstruct(screening_rdb.id),
            )

            screening: Screening = Screening.reconstruct(
                screening_id=ScreeningId.reconstruct(screening_rdb.id),
                apply_date=screening_rdb.apply_date,
                status=ScreeningStatus(screening_rdb.status),
                applicant_email_address=screening_rdb.applicant_email_address,
                interviews=interviews_obj,
            )
            screenings.append(screening)
        return screenings

    def save(self, screening: Screening) -> None:
        result: Tuple[ScreeningRDB, bool] = ScreeningRDB.objects.update_or_create(
            id=screening.screening_id.get_value(),
            defaults=dict(
                apply_date=screening.apply_date,
                status=screening.status.value,
                applicant_email_address=screening.applicant_email_address,
            ),
        )
        screening_rdb = result[0]

        for interview in screening.interviews.interviews:
            recrouter_rdb: RecruiterRDB = RecruiterRDB.objects.get(
                id=interview.recruiter_id
            )

            InterviewRDB.objects.update_or_create(
                id=interview.interview_id.get_value(),
                defaults=dict(
                    screening=screening_rdb,
                    interview_date=interview.interview_date,
                    interview_number=interview.interview_number,
                    screening_step_result=interview.screening_step_result.value,
                    recruiter=recrouter_rdb,
                ),
            )
