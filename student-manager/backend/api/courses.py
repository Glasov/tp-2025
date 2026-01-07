"""
API endpoints для управления курсами
"""
from fastapi import APIRouter, HTTPException, status
from typing import List

from domain.schemas import CourseCreate, CourseResponse
from domain.models import Course
from infrastructure.repositories import course_repo

# Создаём роутер
router = APIRouter(prefix="/courses", tags=["courses"])

@router.get("/", response_model=List[CourseResponse])
async def get_all_courses():
    """Получить все курсы"""
    courses = course_repo.get_all()
    if not courses:
        # Добавляем тестовые курсы если база пуста
        test_courses = [
            Course("CS101", "Введение в программирование", 4),
            Course("MATH201", "Высшая математика", 5),
            Course("ENG301", "Английский язык", 3)
        ]
        for course in test_courses:
            course_repo.add(course)
        courses = test_courses
    
    return courses

@router.get("/{course_id}", response_model=CourseResponse)
async def get_course(course_id: str):
    """Получить курс по ID"""
    course = course_repo.get_by_id(course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Курс с ID {course_id} не найден"
        )
    return course

@router.post("/", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
async def create_course(course_data: CourseCreate):
    """Создать новый курс"""
    # Проверяем уникальность кода курса
    existing_course = course_repo.get_by_code(course_data.code)
    if existing_course:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Курс с таким кодом уже существует"
        )
    
    # Создаём курс
    new_course = Course(
        code=course_data.code,
        name=course_data.name,
        credits=course_data.credits
    )
    
    course_repo.add(new_course)
    return new_course

@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(course_id: str):
    """Удалить курс"""
    success = course_repo.delete(course_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Курс с ID {course_id} не найден"
        )