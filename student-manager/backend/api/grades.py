"""
API endpoints для управления оценками
"""
from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional

from domain.schemas import GradeCreate, GradeResponse
from domain.models import Grade
from infrastructure.repositories import grade_repo, student_repo, course_repo

# Создаём роутер
router = APIRouter(prefix="/grades", tags=["grades"])

@router.get("/", response_model=List[GradeResponse])
async def get_all_grades(
    student_id: Optional[str] = Query(None, description="Фильтр по ID студента"),
    course_id: Optional[str] = Query(None, description="Фильтр по ID курса"),
    min_score: Optional[float] = Query(None, ge=0, le=100, description="Минимальный балл"),
    max_score: Optional[float] = Query(None, ge=0, le=100, description="Максимальный балл")
):
    """Получить все оценки с возможностью фильтрации"""
    grades = grade_repo.get_all()
    
    # Применяем фильтры
    if student_id:
        grades = [g for g in grades if g.student_id == student_id]
    
    if course_id:
        grades = [g for g in grades if g.course_id == course_id]
    
    if min_score is not None:
        grades = [g for g in grades if g.score >= min_score]
    
    if max_score is not None:
        grades = [g for g in grades if g.score <= max_score]
    
    return grades

@router.get("/{grade_id}", response_model=GradeResponse)
async def get_grade(grade_id: str):
    """Получить оценку по ID"""
    grade = grade_repo.get_by_id(grade_id)
    if not grade:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Оценка с ID {grade_id} не найден"
        )
    return grade

@router.post("/", response_model=GradeResponse, status_code=status.HTTP_201_CREATED)
async def create_grade(grade_data: GradeCreate):
    """Создать новую оценку"""
    # Проверяем существует ли студент
    student = student_repo.get_by_id(grade_data.student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Студент с ID {grade_data.student_id} не найден"
        )
    
    # Проверяем существует ли курс
    course = course_repo.get_by_id(grade_data.course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Курс с ID {grade_data.course_id} не найден"
        )
    
    # Создаём оценку
    new_grade = Grade(
        student_id=grade_data.student_id,
        course_id=grade_data.course_id,
        score=grade_data.score
    )
    
    grade_repo.add(new_grade)
    
    return new_grade

@router.put("/{grade_id}", response_model=GradeResponse)
async def update_grade(grade_id: str, score: float = Query(..., ge=0, le=100)):
    """Обновить оценку"""
    grade = grade_repo.get_by_id(grade_id)
    if not grade:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Оценка с ID {grade_id} не найдена"
        )
    
    updated_grade = grade_repo.update(grade_id, score)
    if not updated_grade:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при обновлении оценки"
        )
    
    return updated_grade

@router.delete("/{grade_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_grade(grade_id: str):
    """Удалить оценку"""
    grade = grade_repo.get_by_id(grade_id)
    if not grade:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Оценка с ID {grade_id} не найдена"
        )
    
    success = grade_repo.delete(grade_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при удалении оценки"
        )