"""
Финальная проверка работоспособности проекта
"""
import requests
import json
import os

BASE_URL = "http://localhost:8001"

def check_endpoints():
    print("=" * 60)
    print("ФИНАЛЬНАЯ ПРОВЕРКА STUDENT MANAGER API")
    print("=" * 60)
    
    endpoints_to_check = [
        ("/", "GET", None, "Корневой endpoint"),
        ("/health", "GET", None, "Health check"),
        ("/students/", "GET", None, "Получить студентов"),
        ("/courses/", "GET", None, "Получить курсы"),
        ("/grades/", "GET", None, "Получить оценки"),
        ("/reports/students/summary", "GET", None, "Отчет по студентам"),
        ("/reports/courses/summary", "GET", None, "Отчет по курсам"),
        ("/reports/grades/statistics", "GET", None, "Статистика оценок"),
    ]
    
    all_passed = True
    
    for endpoint, method, data, description in endpoints_to_check:
        try:
            if method == "GET":
                response = requests.get(f"{BASE_URL}{endpoint}")
            elif method == "POST" and data:
                response = requests.post(f"{BASE_URL}{endpoint}", json=data)
            else:
                continue
            
            if 200 <= response.status_code < 300:
                print(f"✅ {description}: {response.status_code}")
            else:
                print(f"❌ {description}: {response.status_code}")
                all_passed = False
                
        except Exception as e:
            print(f"❌ {description}: Ошибка - {str(e)}")
            all_passed = False
    
    print("\n" + "=" * 60)
    
    # Проверяем файлы данных
    print("\nПРОВЕРКА ФАЙЛОВ ДАННЫХ:")
    data_files = ["students.json", "courses.json", "grades.json"]
    
    for file in data_files:
        if os.path.exists(file):
            with open(file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"✅ {file}: {len(data)} записей")
        else:
            print(f"⚠️  {file}: файл не найден (будет создан при добавлении данных)")
    
    print("\n" + "=" * 60)
    
    if all_passed:
        print("\n🎉 ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ УСПЕШНО!")
        print("Проект готов к использованию.")
    else:
        print("\n⚠️  НЕКОТОРЫЕ ПРОВЕРКИ НЕ ПРОЙДЕНЫ")
        print("Проверьте настройки сервера.")
    
    print("\nДокументация доступна по адресу: http://localhost:8001/docs")
    print("ReDoc документация: http://localhost:8001/redoc")

if __name__ == "__main__":
    check_endpoints()