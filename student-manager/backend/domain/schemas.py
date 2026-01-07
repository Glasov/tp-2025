from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# Простые схемы без сложной валидации для совместимости с pydantic v1

# Student Schemas
class StudentBase(BaseModel):
    name: str
    email: str


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None


class StudentInDB(StudentBase):
    student_id: str
    gpa: Optional[float] = None
    created_at: datetime


# Course Schemas
class CourseBase(BaseModel):
    code: str
    name: str
    credits: int


class CourseCreate(CourseBase):
    pass


class CourseInDB(CourseBase):
    course_id: str


# Grade Schemas
class GradeBase(BaseModel):
    student_id: str
    course_id: str
    score: float


class GradeCreate(GradeBase):
    pass


class GradeInDB(GradeBase):
    grade_id: str
    letter_grade: str
    date: datetime


# Response Schemas
class StudentResponse(StudentInDB):
    class Config:
        orm_mode = True


class CourseResponse(CourseInDB):
    class Config:
        orm_mode = True


class GradeResponse(GradeInDB):
    class Config:
        orm_mode = True