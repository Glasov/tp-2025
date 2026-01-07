"""
API endpoints для управления студентами
"""
from fastapi import APIRouter, HTTPException, status
from typing import List

from domain.schemas import StudentCreate, StudentUpdate, StudentResponse
from domain.models import Student
from infrastructure.repositories import student_repo

# Создаём роутер
router = APIRouter(prefix="/students", tags=["students"])

@router.get("/", response_model=List[StudentResponse])
async def get_all_students():
    """Получить всех студентов"""
    students = student_repo.get_all()
    if not students:
        # Добавляем тестовых студентов если база пуста
        test_students = [
            Student("Иван Иванов", "ivan@example.com"),
            Student("Мария Петрова", "maria@example.com"),
            Student("Алексей Сидоров", "alex@example.com")
        ]
        for student in test_students:
            student_repo.add(student)
        students = test_students
    
    return students

@router.get("/{student_id}", response_model=StudentResponse)
async def get_student(student_id: str):
    """Получить студента по ID"""
    student = student_repo.get_by_id(student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Студент с ID {student_id} не найден"
        )
    return student

@router.post("/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
async def create_student(student_data: StudentCreate):
    """Создать нового студента"""
    # Проверяем уникальность email
    existing_student = student_repo.get_by_email(student_data.email)
    if existing_student:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Студент с таким email уже существует"
        )
    
    # Создаём студента
    new_student = Student(
        name=student_data.name,
        email=student_data.email
    )
    
    student_repo.add(new_student)
    return new_student

@router.put("/{student_id}", response_model=StudentResponse)
async def update_student(student_id: str, student_data: StudentUpdate):
    """Обновить данные студента"""
    student = student_repo.get_by_id(student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Студент с ID {student_id} не найден"
        )
    
    # Проверяем уникальность нового email если он изменяется
    if student_data.email is not None and student_data.email != student.email:
        existing_student = student_repo.get_by_email(student_data.email)
        if existing_student:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Студент с таким email уже существует"
            )
    
    # Обновляем поля
    update_data = {}
    if student_data.name is not None:
        update_data['name'] = student_data.name
    if student_data.email is not None:
        update_data['email'] = student_data.email
    
    updated_student = student_repo.update(student_id, **update_data)
    if not updated_student:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при обновлении студента"
        )
    
    return updated_student

@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(student_id: str):
    """Удалить студента"""
    success = student_repo.delete(student_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Студент с ID {student_id} не найден"
        )