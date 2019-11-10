from datetime import date
from uuid import UUID
from typing import Any, List

from .entities import Screening, ScreeningId, Recruiter, RecruiterId
from .repositories import ScreeningRepository, RecruiterRepository
from .repository_interfaces import (
    ScreeningRepositoryInterface,
    RecruiterRepositoryInterface,
)


class ScreeningApplicationService:
    screening_repository: ScreeningRepositoryInterface = ScreeningRepository()

    def start_from_pre_interview(self, applicant_email_address: Any) -> None:
        screening: Screening = Screening.start_from_pre_interview(
            applicant_email_address
        )
        self.screening_repository.save(screening)

    def apply(self, applicant_email_address: Any) -> None:
        screening: Screening = Screening.apply(applicant_email_address)
        self.screening_repository.save(screening)

    def add_next_interview(
        self, screening_id: UUID, interview_date: date, recruiter_id: UUID
    ) -> None:
        screening: Screening = self.screening_repository.get(
            screening_id=ScreeningId.reconstruct(screening_id)
        )
        screening.add_next_interview(
            interview_date=interview_date,
            recruiter_id=RecruiterId.reconstruct(recruiter_id),
        )

    def get_all_screenings(self) -> List[Screening]:
        return self.screening_repository.get_all()

    def get_screening(self, screening_id: UUID) -> Screening:
        return self.screening_repository.get(
            screening_id=ScreeningId.reconstruct(screening_id)
        )


class RecruiterApplicationService:
    recruiter_repository: RecruiterRepositoryInterface = RecruiterRepository()

    def get_all_recruiters(self) -> List[Recruiter]:
        return self.recruiter_repository.get_all()
