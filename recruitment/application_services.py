from typing import Any, List

from .entities import Screening
from .repositories import ScreeningRepository
from .repository_interfaces import ScreeningRepositoryInterface


class ScreeningApplicationService:
    screening_repository: ScreeningRepositoryInterface = ScreeningRepository()

    def start_from_pre_interview(self, applicant_email_address: Any) -> None:
        screening: Screening = Screening.start_from_pre_interview(
            applicant_email_address
        )
        self.screening_repository.save(screening)

    def apply(self, applicant_email_address: Any) -> None:
        screening: Screening = Screening.apply(
            applicant_email_address
        )
        self.screening_repository.save(screening)

    def get_all(self) -> List[Screening]:
        return self.screening_repository.get_all()
