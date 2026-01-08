import requests
import json

BASE_URL = "http://localhost:8001"

# 1. Создаём студента с русским именем
student_data = {
    "name": "Анна Сидорова",
    "email": "anna@example.com"
}

response = requests.post(f"{BASE_URL}/students/", 
                        json=student_data,
                        headers={"Content-Type": "application/json"})
print("1. Создание студента:")
print(f"   Status: {response.status_code}")
print(f"   Response: {response.json()}")
print()

# 2. Получаем всех студентов
response = requests.get(f"{BASE_URL}/students/")
print("2. Все студенты:")
students = response.json()
for student in students:
    print(f"   - {student['name']} ({student['email']})")
print()

# 3. Получаем курсы
response = requests.get(f"{BASE_URL}/courses/")
print("3. Все курсы:")
courses = response.json()
for course in courses:
    print(f"   - {course['code']}: {course['name']} ({course['credits']} кредитов)")