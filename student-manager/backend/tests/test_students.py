"""
Тесты для студентов
"""
import pytest
from fastapi.testclient import TestClient
from domain.models import Student

# Будем использовать TestClient для тестирования API
# В реальном проекте нужно настроить фикстуры для тестовой базы данных

def test_student_creation():
    """Тест создания студента"""
    student = Student(name="Тест Студент", email="test@example.com")
    
    assert student.name == "Тест Студент"
    assert student.email == "test@example.com"
    assert student.student_id is not None
    assert student.created_at is not None

def test_student_update_gpa():
    """Тест обновления GPA студента"""
    student = Student(name="Тест", email="test@example.com")
    
    # Корректное значение
    student.update_gpa(4.5)
    assert student.gpa == 4.5
    
    # Некорректное значение
    with pytest.raises(ValueError):
        student.update_gpa(6.0)

def test_student_equality():
    """Тест сравнения студентов"""
    student1 = Student(name="Студент 1", email="test1@example.com")
    student2 = Student(name="Студент 2", email="test2@example.com")
    
    assert student1 != student2
    assert student1.student_id != student2.student_id

if __name__ == "__main__":
    pytest.main([__file__])