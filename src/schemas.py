from enum import Enum

from pydantic import BaseModel, Field


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"


class RaceEthnicity(str, Enum):
    GROUP_A = "group A"
    GROUP_B = "group B"
    GROUP_C = "group C"
    GROUP_D = "group D"
    GROUP_E = "group E"


class ParentEducation(str, Enum):
    ASSOCIATES_DEGREE = "associate's degree"
    BACHELORS_DEGREE = "bachelor's degree"
    HIGH_SCHOOL = "high school"
    MASTERS_DEGREE = "master's degree"
    SOME_COLLEGE = "some college"
    SOME_HIGH_SCHOOL = "some high school"


class Lunch(str, Enum):
    STANDARD = "standard"
    FREE_REDUCED = "free/reduced"


class TestPreparationCourse(str, Enum):
    NONE = "none"
    COMPLETED = "completed"


class PredictRequest(BaseModel):
    gender: Gender
    race_ethnicity: RaceEthnicity
    parent_education: ParentEducation
    lunch: Lunch
    test_preparation_course: TestPreparationCourse
    reading_score: float = Field(ge=0, le=100)
    writing_score: float = Field(ge=0, le=100)
