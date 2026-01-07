
import requests
import json
import os

BASE_URL = "http://localhost:8001"

def test_student_creation():
    """Тестируем создание студента с кириллицей"""
    
    # Создаём студента
    student_data = {
        "name": "Иван Петров",
        "email": "ivan.petrov2@example.com"
    }
    
    print("Создаём студента...")
    response = requests.post(f"{BASE_URL}/students/", 
                            json=student_data)
    
    if response.status_code == 201:
        student = response.json()
        print(f"Успешно создан: {student['name']}")
        print(f"ID: {student['student_id']}")
    else:
        print(f"Ошибка: {response.status_code}")
        print(response.text)
    
    # Проверяем файл
    if os.path.exists("students.json"):
        print("\nСодержимое файла students.json:")
        with open("students.json", "r", encoding="utf-8") as f:
            content = f.read()
            print(content)
            
            # Проверяем есть ли кириллица
            if "Иван" in content:
                print("\n✅ Кириллица сохранилась правильно!")
            else:
                print("\n❌ Проблема с кодировкой!")
    else:
        print("Файл students.json не найден")

if __name__ == "__main__":
    test_student_creation()