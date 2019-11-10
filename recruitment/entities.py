from datetime import date
from uuid import uuid4, UUID
from enum import Enum, auto

from typing import Any, List, Union


class EntityId:
    value: UUID

    def __init__(self) -> None:
        self.value = uuid4()

    @classmethod
    def reconstruct(cls, value: UUID) -> "EntityId":
        entity_id: "EntityId" = cls()
        entity_id.value = value
        return entity_id

    def get_value(self) -> UUID:
        return self.value

    def get_str_value(self) -> str:
        return str(self.value)


class ScreeningId(EntityId):
    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def reconstruct(cls, value: UUID) -> "ScreeningId":
        screening_id: "ScreeningId" = cls()
        screening_id.value = value
        return screening_id


class InterviewId(EntityId):
    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def reconstruct(cls, value: UUID) -> "InterviewId":
        interview_id: "InterviewId" = cls()
        interview_id.value = value
        return interview_id


class RecruiterId(EntityId):
    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def reconstruct(cls, value: UUID) -> "RecruiterId":
        recruiter_id: "RecruiterId" = cls()
        recruiter_id.value = value
        return recruiter_id


class ScreeningStatus(Enum):
    not_applied: auto = auto()
    interview: auto = auto()
    rejected: auto = auto()
    passed: auto = auto()

    def can_add_interview(self):
        if self.name == "not_applied":
            return False
        if self.name == "interview":
            return True
        if self.name == "rejected":
            return False
        if self.name == "passed":
            return False
        raise Exception("不正なstatusです。")


class ScreeningStepResult(Enum):
    unrated: auto = auto()
    passed: auto = auto()
    failure: auto = auto()

    def can_add_interview(self):
        if self.name == "not_applied":
            return False
        if self.name == "passed":
            return False
        if self.name == "failure":
            return False
        raise Exception("不正なresultです。")


class Screening:
    screening_id: ScreeningId
    apply_date: date
    status: ScreeningStatus
    applicant_email_address: Any
    interviews: "Interviews"

    @staticmethod
    def reconstruct(
        screening_id: ScreeningId,
        apply_date: date,
        status: ScreeningStatus,
        applicant_email_address: Any,
        interviews: "Interviews",
    ) -> "Screening":
        screening: "Screening" = Screening()
        screening.screening_id = screening_id
        screening.apply_date = apply_date
        screening.applicant_email_address = applicant_email_address
        screening.status = status
        screening.interviews = interviews
        return screening

    @classmethod
    def apply(cls, applicant_email_address: Any) -> "Screening":
        screening: "Screening" = Screening()
        screening.screening_id = ScreeningId()
        screening.apply_date = date.today()
        screening.applicant_email_address = applicant_email_address
        screening.status = ScreeningStatus.not_applied
        screening.interviews = Interviews(screening_id=screening.screening_id)
        return screening

    @classmethod
    def start_from_pre_interview(cls, applicant_email_address: Any) -> "Screening":
        screening: "Screening" = Screening()
        screening.screening_id = ScreeningId()

        screening.apply_date = date.today()
        screening.applicant_email_address = applicant_email_address
        screening.status = ScreeningStatus.interview
        return screening

    def add_next_interview(
        self, interview_date: date, recruiter_id: RecruiterId
    ) -> None:
        self.interviews.add_next_interview(interview_date, recruiter_id)


class Interview:
    interview_id: InterviewId
    screening_id: ScreeningId
    interview_date: date
    interview_number: int
    screening_step_result: ScreeningStepResult
    recruiter_id: RecruiterId

    def __init__(
        self,
        screening_id: ScreeningId,
        interview_date: date,
        interview_number: int,
        recruiter_id: RecruiterId,
    ) -> None:
        self.interview_id = InterviewId()
        self.screening_id = screening_id
        self.interview_date = date.today()
        self.interview_number = interview_number
        self.screening_step_result = ScreeningStepResult.unrated
        self.recruiter_id = recruiter_id

    @staticmethod
    def reconstruct(
        interview_id: InterviewId,
        screening_id: ScreeningId,
        interview_date: date,
        interview_number: int,
        screening_step_result: ScreeningStepResult,
        recruiter_id: RecruiterId,
    ) -> "Interview":
        interview: "Interview" = Interview(
            screening_id=screening_id,
            interview_date=interview_date,
            interview_number=interview_number,
            recruiter_id=recruiter_id,
        )
        interview.interview_id = interview_id
        interview.screening_step_result = screening_step_result
        return interview


class Interviews:
    interviews: List[Interview]
    screening_id: ScreeningId

    def __init__(self, screening_id: ScreeningId) -> None:
        self.interviews = []
        self.screening_id = screening_id

    @staticmethod
    def reconstruct(
        interviews: List[Interview], screening_id: ScreeningId
    ) -> "Interviews":
        interviews_obj: "Interviews" = Interviews(screening_id)
        interviews_obj.interviews = interviews
        return interviews_obj

    def add_next_interview(
        self, interview_date: date, recruiter_id: RecruiterId
    ) -> None:
        interview_number = self.get_next_interview_number()
        interview = Interview(
            self.screening_id, interview_date, interview_number, recruiter_id
        )
        self.interviews.append(interview)

    def get_next_interview_number(self) -> int:
        return len(self.interviews) + 1

    def get_latest_interview(self) -> Union[Interview, None]:
        if self.interviews == []:
            return None
        return self.interviews[-1]


class Recruiter:
    recruiter_id: RecruiterId
    name: str

    def __init__(self, name: str):
        self.recruiter_id = RecruiterId()
        self.name = name

    @staticmethod
    def reconstruct(recruiter_id: RecruiterId, name: str) -> "Recruiter":
        recruiter: "Recruiter" = Recruiter(name=name)
        recruiter.recruiter_id = recruiter_id
        return recruiter
