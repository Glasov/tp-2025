import requests
import json

BASE_URL = "http://localhost:8001"

def test_grades_api():
    print("=== Тестирование API оценок ===\n")
    
    # 1. Получаем студентов и курсы для теста
    print("1. Получаем существующих студентов...")
    response = requests.get(f"{BASE_URL}/students/")
    students = response.json()
    if not students:
        print("   Нет студентов, создаём тестового...")
        student_data = {"name": "Тест Студент", "email": "test@grades.com"}
        response = requests.post(f"{BASE_URL}/students/", json=student_data)
        student = response.json()
        student_id = student['student_id']
    else:
        student = students[0]
        student_id = student['student_id']
    
    print(f"   Студент: {student['name']} (ID: {student_id})\n")
    
    print("2. Получаем существующие курсы...")
    response = requests.get(f"{BASE_URL}/courses/")
    courses = response.json()
    if not courses:
        print("   Нет курсов, создаём тестовый...")
        course_data = {"code": "TEST101", "name": "Тестовый курс", "credits": 3}
        response = requests.post(f"{BASE_URL}/courses/", json=course_data)
        course = response.json()
        course_id = course['course_id']
    else:
        course = courses[0]
        course_id = course['course_id']
    
    print(f"   Курс: {course['name']} (ID: {course_id})\n")
    
    # 3. Создаём оценку
    print("3. Создаём оценку...")
    grade_data = {
        "student_id": student_id,
        "course_id": course_id,
        "score": 85.5
    }
    
    response = requests.post(f"{BASE_URL}/grades/", json=grade_data)
    if response.status_code == 201:
        grade = response.json()
        print(f"   ✅ Оценка создана: {grade['score']} баллов")
        print(f"   Буквенная оценка: {grade['letter_grade']}")
        print(f"   ID оценки: {grade['grade_id']}\n")
        grade_id = grade['grade_id']
    else:
        print(f"   ❌ Ошибка: {response.status_code}")
        print(f"   {response.text}")
        return
    
    # 4. Получаем все оценки студента
    print("4. Получаем оценки студента...")
    response = requests.get(f"{BASE_URL}/grades/student/{student_id}")
    student_grades = response.json()
    print(f"   У студента {len(student_grades)} оценок")
    
    # 5. Получаем все оценки с фильтрацией
    print("\n5. Тестируем фильтрацию оценок...")
    response = requests.get(f"{BASE_URL}/grades/?min_score=80&max_score=90")
    filtered_grades = response.json()
    print(f"   Найдено оценок от 80 до 90 баллов: {len(filtered_grades)}")
    
    # 6. Обновляем GPA студента
    print("\n6. Проверяем обновление GPA студента...")
    response = requests.get(f"{BASE_URL}/students/{student_id}")
    updated_student = response.json()
    print(f"   GPA студента: {updated_student.get('gpa', 'не рассчитан')}")
    
    print("\n=== Тест завершён ===")

if __name__ == "__main__":
    test_grades_api()