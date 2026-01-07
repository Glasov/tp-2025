"""
Тесты для курсов
"""
from domain.models import Course

def test_course_creation():
    """Тест создания курса"""
    course = Course(code="CS101", name="Программирование", credits=4)
    
    assert course.code == "CS101"
    assert course.name == "Программирование"
    assert course.credits == 4
    assert course.course_id is not None

def test_course_attributes():
    """Тест атрибутов курса"""
    course = Course(code="MATH201", name="Математика", credits=5)
    
    assert hasattr(course, 'code')
    assert hasattr(course, 'name')
    assert hasattr(course, 'credits')
    assert hasattr(course, 'course_id')