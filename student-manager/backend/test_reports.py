import requests
import json

BASE_URL = "http://localhost:8001"

def test_reports():
    print("=== Тестирование отчетов ===\n")
    
    # 1. Получаем ID студента и курса для теста
    print("1. Получаем данные для теста...")
    
    # Студенты
    response = requests.get(f"{BASE_URL}/students/")
    students = response.json()
    student_id = students[0]['student_id'] if students else None
    
    # Курсы
    response = requests.get(f"{BASE_URL}/courses/")
    courses = response.json()
    course_id = courses[0]['course_id'] if courses else None
    
    if not student_id or not course_id:
        print("   Недостаточно данных для теста")
        return
    
    print(f"   Студент ID: {student_id}")
    print(f"   Курс ID: {course_id}\n")
    
    # 2. Сводка по студентам
    print("2. Тестируем сводку по студентам...")
    response = requests.get(f"{BASE_URL}/reports/students/summary")
    if response.status_code == 200:
        data = response.json()
        print(f"   Всего студентов: {data['total_students']}")
        for student in data['students'][:3]:  # Показываем первых 3
            print(f"   - {student['name']}: GPA {student['gpa']}, оценок: {student['grades_count']}")
    print()
    
    # 3. Сводка по курсам
    print("3. Тестируем сводку по курсам...")
    response = requests.get(f"{BASE_URL}/reports/courses/summary")
    if response.status_code == 200:
        data = response.json()
        print(f"   Всего курсов: {data['total_courses']}")
        for course in data['courses'][:3]:  # Показываем первые 3
            print(f"   - {course['code']}: {course['name']}, оценок: {course['grades_count']}")
    print()
    
    # 4. Статистика по оценкам
    print("4. Тестируем статистику по оценкам...")
    response = requests.get(f"{BASE_URL}/reports/grades/statistics")
    if response.status_code == 200:
        data = response.json()
        print(f"   Всего оценок: {data['total_grades']}")
        print(f"   Средний балл: {data['average_score']}")
        print(f"   Распределение: {data['grade_distribution']}")
    print()
    
    # 5. Топ студентов
    print("5. Тестируем топ студентов...")
    response = requests.get(f"{BASE_URL}/reports/top/students?limit=5")
    if response.status_code == 200:
        data = response.json()
        print(f"   Топ {data['limit']} студентов:")
        for i, student in enumerate(data['students'], 1):
            print(f"   {i}. {student['name']}: GPA {student.get('gpa', 'N/A')}")
    print()
    
    # 6. Прогресс студента
    print("6. Тестируем прогресс студента...")
    response = requests.get(f"{BASE_URL}/reports/student/{student_id}/progress")
    if response.status_code == 200:
        data = response.json()
        print(f"   Студент: {data['student_name']}")
        print(f"   GPA: {data['gpa']}")
        print(f"   Курсов завершено: {data['courses_completed']}/{data['total_courses']}")
        print(f"   Средневзвешенный балл: {data['weighted_average']}")
    else:
        print(f"   Ошибка: {response.status_code}")
        print(f"   {response.text}")
    
    print("\n=== Тест отчетов завершён ===")

if __name__ == "__main__":
    test_reports()