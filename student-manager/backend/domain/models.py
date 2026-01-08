from datetime import datetime
from typing import Optional, List
from uuid import UUID, uuid4


class Student:
    def __init__(self, name: str, email: str, student_id: Optional[str] = None):
        self.student_id = student_id or str(uuid4())
        self.name = name
        self.email = email
        self.created_at = datetime.now()
        self.gpa: Optional[float] = None

    def update_gpa(self, gpa: float):
        if 0 <= gpa <= 5.0:
            self.gpa = gpa
        else:
            raise ValueError("GPA должен быть от 0 до 5.0")


class Course:
    def __init__(self, code: str, name: str, credits: int, course_id: Optional[str] = None):
        self.course_id = course_id or str(uuid4())
        self.code = code
        self.name = name
        self.credits = credits


class Grade:
    def __init__(self, student_id: str, course_id: str, score: float, grade_id: Optional[str] = None):
        self.grade_id = grade_id or str(uuid4())
        self.student_id = student_id
        self.course_id = course_id
        self.score = score
        self.date = datetime.now()
        
        
        if score >= 90:
            self.letter_grade = '5'
        elif score >= 80:
            self.letter_grade = '4'
        elif score >= 70:
            self.letter_grade = '3'
        elif score >= 60:
            self.letter_grade = '2'
        else:
            self.letter_grade = '1'