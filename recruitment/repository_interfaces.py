from typing import List
from typing_extensions import Protocol

from .entities import Screening, ScreeningId


class ScreeningRepositoryInterface(Protocol):
    def get(self, screening_id: ScreeningId) -> Screening:
        ...

    def get_all(self) -> List[Screening]:
        ...

    def save(self, screening: Screening) -> None:
        ...
