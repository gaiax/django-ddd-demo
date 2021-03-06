from typing import List
from typing_extensions import Protocol

from .entities import Screening, ScreeningId, Recruiter, RecruiterId


class ScreeningRepositoryInterface(Protocol):
    def get(self, screening_id: ScreeningId) -> Screening:
        ...

    def get_all(self) -> List[Screening]:
        ...

    def save(self, screening: Screening) -> None:
        ...


class RecruiterRepositoryInterface(Protocol):
    def get(self, recruiter_id: RecruiterId) -> Recruiter:
        ...

    def get_all(self) -> List[Recruiter]:
        ...

    def save(self, recruiter: Recruiter) -> None:
        ...
