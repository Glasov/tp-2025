"""
Репозитории для работы с данными
"""
import json
import os
from typing import List, Optional, Dict, Any
from domain.models import Student, Course, Grade
from datetime import datetime


class StudentRepository:
    def __init__(self, file_path: str = "students.json"):
        self.file_path = file_path
        self.students: Dict[str, Student] = {}
        self._load_from_file()
    
    def _load_from_file(self):
        """Загрузить студентов из файла"""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for student_data in data:
                        # Конвертируем строку даты обратно в datetime
                        created_at_str = student_data['created_at']
                        if isinstance(created_at_str, str):
                            try:
                                created_at = datetime.fromisoformat(created_at_str)
                            except (ValueError, AttributeError):
                                created_at = datetime.now()
                        else:
                            created_at = datetime.now()
                        
                        student = Student(
                            name=student_data['name'],
                            email=student_data['email'],
                            student_id=student_data['student_id']
                        )
                        student.created_at = created_at
                        student.gpa = student_data.get('gpa')
                        self.students[student.student_id] = student
            except Exception as e:
                print(f"Ошибка загрузки студентов: {e}")
                # Если файл повреждён, начинаем с чистого листа
                self.students = {}
    
    def _save_to_file(self):
        """Сохранить студентов в файл"""
        try:
            data = []
            for student in self.students.values():
                # Конвертируем datetime в строку для JSON
                created_at_str = student.created_at.isoformat() if hasattr(student.created_at, 'isoformat') else datetime.now().isoformat()
                
                data.append({
                    'student_id': student.student_id,
                    'name': student.name,
                    'email': student.email,
                    'created_at': created_at_str,
                    'gpa': student.gpa
                })
            
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения студентов: {e}")
    
    def get_all(self) -> List[Student]:
        """Получить всех студентов"""
        return list(self.students.values())
    
    def get_by_id(self, student_id: str) -> Optional[Student]:
        """Получить студента по ID"""
        return self.students.get(student_id)
    
    def get_by_email(self, email: str) -> Optional[Student]:
        """Получить студента по email"""
        for student in self.students.values():
            if student.email == email:
                return student
        return None
    
    def add(self, student: Student) -> Student:
        """Добавить нового студента"""
        self.students[student.student_id] = student
        self._save_to_file()
        return student
    
    def update(self, student_id: str, **kwargs) -> Optional[Student]:
        """Обновить данные студента"""
        student = self.students.get(student_id)
        if student:
            for key, value in kwargs.items():
                if value is not None and hasattr(student, key):
                    setattr(student, key, value)
            self._save_to_file()
        return student
    
    def delete(self, student_id: str) -> bool:
        """Удалить студента"""
        if student_id in self.students:
            del self.students[student_id]
            self._save_to_file()
            return True
        return False


class CourseRepository:
    def __init__(self, file_path: str = "courses.json"):
        self.file_path = file_path
        self.courses: Dict[str, Course] = {}
        self._load_from_file()
    
    def _load_from_file(self):
        """Загрузить курсы из файла"""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for course_data in data:
                        course = Course(
                            code=course_data['code'],
                            name=course_data['name'],
                            credits=course_data['credits'],
                            course_id=course_data['course_id']
                        )
                        self.courses[course.course_id] = course
            except Exception as e:
                print(f"Ошибка загрузки курсов: {e}")
                self.courses = {}
    
    def _save_to_file(self):
        """Сохранить курсы в файл"""
        try:
            data = []
            for course in self.courses.values():
                data.append({
                    'course_id': course.course_id,
                    'code': course.code,
                    'name': course.name,
                    'credits': course.credits
                })
            
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения курсов: {e}")
    
    def get_all(self) -> List[Course]:
        """Получить все курсы"""
        return list(self.courses.values())
    
    def get_by_id(self, course_id: str) -> Optional[Course]:
        """Получить курс по ID"""
        return self.courses.get(course_id)
    
    def get_by_code(self, code: str) -> Optional[Course]:
        """Получить курс по коду"""
        for course in self.courses.values():
            if course.code == code:
                return course
        return None
    
    def add(self, course: Course) -> Course:
        """Добавить новый курс"""
        self.courses[course.course_id] = course
        self._save_to_file()
        return course
    
    def delete(self, course_id: str) -> bool:
        """Удалить курс"""
        if course_id in self.courses:
            del self.courses[course_id]
            self._save_to_file()
            return True
        return False


# Создаём глобальные экземпляры репозиториев
student_repo = StudentRepository()
course_repo = CourseRepository()
class GradeRepository:
    def __init__(self, file_path: str = "grades.json"):
        self.file_path = file_path
        self.grades: Dict[str, Grade] = {}
        self._load_from_file()
    
    def _load_from_file(self):
        """Загрузить оценки из файла"""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for grade_data in data:
                        # Конвертируем строку даты обратно в datetime
                        date_str = grade_data['date']
                        if isinstance(date_str, str):
                            try:
                                date = datetime.fromisoformat(date_str)
                            except (ValueError, AttributeError):
                                date = datetime.now()
                        else:
                            date = datetime.now()
                        
                        grade = Grade(
                            student_id=grade_data['student_id'],
                            course_id=grade_data['course_id'],
                            score=grade_data['score'],
                            grade_id=grade_data['grade_id']
                        )
                        grade.date = date
                        grade.letter_grade = grade_data.get('letter_grade', 'F')
                        self.grades[grade.grade_id] = grade
            except Exception as e:
                print(f"Ошибка загрузки оценок: {e}")
                self.grades = {}
    
    def _save_to_file(self):
        """Сохранить оценки в файл"""
        try:
            data = []
            for grade in self.grades.values():
                # Конвертируем datetime в строку для JSON
                date_str = grade.date.isoformat() if hasattr(grade.date, 'isoformat') else datetime.now().isoformat()
                
                data.append({
                    'grade_id': grade.grade_id,
                    'student_id': grade.student_id,
                    'course_id': grade.course_id,
                    'score': grade.score,
                    'letter_grade': grade.letter_grade,
                    'date': date_str
                })
            
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения оценок: {e}")
    
    def get_all(self) -> List[Grade]:
        """Получить все оценки"""
        return list(self.grades.values())
    
    def get_by_id(self, grade_id: str) -> Optional[Grade]:
        """Получить оценку по ID"""
        return self.grades.get(grade_id)
    
    def get_by_student(self, student_id: str) -> List[Grade]:
        """Получить оценки студента"""
        return [grade for grade in self.grades.values() if grade.student_id == student_id]
    
    def get_by_course(self, course_id: str) -> List[Grade]:
        """Получить оценки по курсу"""
        return [grade for grade in self.grades.values() if grade.course_id == course_id]
    
    def get_by_student_and_course(self, student_id: str, course_id: str) -> List[Grade]:
        """Получить оценки студента по курсу"""
        return [grade for grade in self.grades.values() 
                if grade.student_id == student_id and grade.course_id == course_id]
    
    def add(self, grade: Grade) -> Grade:
        """Добавить новую оценку"""
        self.grades[grade.grade_id] = grade
        self._save_to_file()
        return grade
    
    def update(self, grade_id: str, score: float) -> Optional[Grade]:
        """Обновить оценку"""
        grade = self.grades.get(grade_id)
        if grade:
            grade.score = score
            
            # Обновляем буквенную оценку
            if score >= 90:
                grade.letter_grade = '5'
            elif score >= 80:
                grade.letter_grade = '4'
            elif score >= 70:
                grade.letter_grade = '3'
            elif score >= 60:
                grade.letter_grade = '2'
            else:
                grade.letter_grade = '1'
                
            self._save_to_file()
        return grade
    
    def delete(self, grade_id: str) -> bool:
        """Удалить оценку"""
        if grade_id in self.grades:
            del self.grades[grade_id]
            self._save_to_file()
            return True
        return False
    
    def calculate_student_gpa(self, student_id: str) -> Optional[float]:
        """Рассчитать GPA студента"""
        student_grades = self.get_by_student(student_id)
        if not student_grades:
            return None
        
        # Простой расчет среднего
        total = sum(grade.score for grade in student_grades)
        return round(total / len(student_grades) / 20, 2)  # Конвертируем в 5-балльную шкалу

# Создаём глобальный экземпляр репозитория оценок
grade_repo = GradeRepository()