"""
API endpoints для отчетов
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Any, Optional
from datetime import datetime

from infrastructure.repositories import student_repo, course_repo, grade_repo

router = APIRouter(prefix="/reports", tags=["reports"])

@router.get("/students/summary")
async def get_students_summary(
    min_gpa: Optional[float] = Query(None, ge=0, le=5, description="Минимальный GPA"),
    max_gpa: Optional[float] = Query(None, ge=0, le=5, description="Максимальный GPA")
):
    """Получить сводку по студентам с фильтрацией по GPA"""
    students = student_repo.get_all()
    grades = grade_repo.get_all()
    
    summary = []
    for student in students:
        student_grades = [g for g in grades if g.student_id == student.student_id]
        
        if student_grades:
            total_score = sum(g.score for g in student_grades)
            avg_score = total_score / len(student_grades)
            gpa = round(avg_score / 20, 2)  # Конвертируем в 5-балльную шкалу
        else:
            avg_score = 0
            gpa = 0
        
        # Применяем фильтрацию по GPA если указана
        if min_gpa is not None and gpa < min_gpa:
            continue
        if max_gpa is not None and gpa > max_gpa:
            continue
        
        summary.append({
            "student_id": student.student_id,
            "name": student.name,
            "email": student.email,
            "grades_count": len(student_grades),
            "average_score": round(avg_score, 2),
            "gpa": gpa,
            "created_at": student.created_at
        })
    
    # Сортируем по GPA (по убыванию)
    summary.sort(key=lambda x: x["gpa"], reverse=True)
    
    return {
        "total_students": len(summary),
        "students": summary
    }

@router.get("/courses/summary")
async def get_courses_summary():
    """Получить сводку по курсам"""
    courses = course_repo.get_all()
    grades = grade_repo.get_all()
    
    summary = []
    for course in courses:
        course_grades = [g for g in grades if g.course_id == course.course_id]
        
        if course_grades:
            total_score = sum(g.score for g in course_grades)
            avg_score = total_score / len(course_grades)
            
            # Распределение оценок
            grade_distribution = {
                "A": len([g for g in course_grades if g.score >= 90]),
                "B": len([g for g in course_grades if g.score >= 80 and g.score < 90]),
                "C": len([g for g in course_grades if g.score >= 70 and g.score < 80]),
                "D": len([g for g in course_grades if g.score >= 60 and g.score < 70]),
                "F": len([g for g in course_grades if g.score < 60])
            }
        else:
            avg_score = 0
            grade_distribution = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}
        
        summary.append({
            "course_id": course.course_id,
            "code": course.code,
            "name": course.name,
            "credits": course.credits,
            "grades_count": len(course_grades),
            "average_score": round(avg_score, 2),
            "grade_distribution": grade_distribution
        })
    
    # Сортируем по количеству оценок (по убыванию)
    summary.sort(key=lambda x: x["grades_count"], reverse=True)
    
    return {
        "total_courses": len(summary),
        "courses": summary
    }

@router.get("/grades/statistics")
async def get_grades_statistics(
    student_id: Optional[str] = Query(None, description="ID студента для фильтрации"),
    course_id: Optional[str] = Query(None, description="ID курса для фильтрации")
):
    """Получить статистику по оценкам"""
    grades = grade_repo.get_all()
    
    # Применяем фильтры
    if student_id:
        grades = [g for g in grades if g.student_id == student_id]
    
    if course_id:
        grades = [g for g in grades if g.course_id == course_id]
    
    if not grades:
        return {
            "total_grades": 0,
            "message": "Нет оценок для отображения"
        }
    
    # Базовая статистика
    scores = [g.score for g in grades]
    
    return {
        "total_grades": len(grades),
        "average_score": round(sum(scores) / len(scores), 2),
        "min_score": round(min(scores), 2),
        "max_score": round(max(scores), 2),
        "grade_distribution": {
            "A (90-100)": len([g for g in grades if g.score >= 90]),
            "B (80-89)": len([g for g in grades if g.score >= 80 and g.score < 90]),
            "C (70-79)": len([g for g in grades if g.score >= 70 and g.score < 80]),
            "D (60-69)": len([g for g in grades if g.score >= 60 and g.score < 70]),
            "F (0-59)": len([g for g in grades if g.score < 60])
        }
    }

@router.get("/top/students")
async def get_top_students(limit: int = Query(10, ge=1, le=100, description="Количество студентов")):
    """Получить топ студентов по GPA"""
    students = student_repo.get_all()
    
    # Сортируем студентов по GPA
    students_with_gpa = []
    for student in students:
        gpa = student.gpa if student.gpa is not None else 0
        students_with_gpa.append({
            "student": student,
            "gpa": gpa
        })
    
    students_with_gpa.sort(key=lambda x: x["gpa"], reverse=True)
    
    # Берем топ N
    top_students = students_with_gpa[:limit]
    
    return {
        "limit": limit,
        "students": [
            {
                "student_id": item["student"].student_id,
                "name": item["student"].name,
                "email": item["student"].email,
                "gpa": item["gpa"],
                "created_at": item["student"].created_at
            }
            for item in top_students
        ]
    }

@router.get("/student/{student_id}/progress")
async def get_student_progress(student_id: str):
    """Получить прогресс студента по всем курсам"""
    student = student_repo.get_by_id(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Студент не найден")
    
    student_grades = grade_repo.get_by_student(student_id)
    courses = course_repo.get_all()
    
    progress = []
    total_credits = 0
    weighted_score_sum = 0
    
    for course in courses:
        course_grades = [g for g in student_grades if g.course_id == course.course_id]
        
        if course_grades:
            avg_score = sum(g.score for g in course_grades) / len(course_grades)
            status = "completed"
        else:
            avg_score = 0
            status = "not_started"
        
        progress.append({
            "course_id": course.course_id,
            "course_code": course.code,
            "course_name": course.name,
            "credits": course.credits,
            "grades_count": len(course_grades),
            "average_score": round(avg_score, 2),
            "status": status
        })
        
        if course_grades:
            total_credits += course.credits
            weighted_score_sum += avg_score * course.credits
    
    # Рассчитываем средневзвешенный балл
    weighted_average = weighted_score_sum / total_credits if total_credits > 0 else 0
    
    return {
        "student_id": student_id,
        "student_name": student.name,
        "total_courses": len(courses),
        "courses_completed": len([p for p in progress if p["status"] == "completed"]),
        "total_credits": total_credits,
        "weighted_average": round(weighted_average, 2),
        "gpa": student.gpa,
        "progress": progress
    }