"""
Паттерн Цепочка обязанностей (Chain of Responsibility)
Позволяет передавать запросы последовательно по цепочке обработчиков.
"""

from abc import ABC, abstractmethod
from typing import Optional, Any



class Handler(ABC):
    """Абстрактный обработчик"""
    def __init__(self):
        self._next_handler: Optional['Handler'] = None
    
    def set_next(self, handler: 'Handler') -> 'Handler':
        """Установка следующего обработчика в цепочке"""
        self._next_handler = handler
        return handler
    
    @abstractmethod
    def handle(self, request: Any) -> Optional[str]:
        """Обработка запроса"""
        if self._next_handler:
            return self._next_handler.handle(request)
        return None


class AuthHandler(Handler):
    """Обработчик аутентификации"""
    def handle(self, request: dict) -> Optional[str]:
        print("🔐 Проверка аутентификации...")
        
        if not request.get("authenticated", False):
            return "❌ Ошибка: Пользователь не аутентифицирован"
        
        print("✅ Аутентификация успешна")
        return super().handle(request)


class PermissionHandler(Handler):
    """Обработчик проверки прав доступа"""
    def handle(self, request: dict) -> Optional[str]:
        print("🔑 Проверка прав доступа...")
        
        required_role = request.get("required_role", "user")
        user_role = request.get("user_role", "guest")
        
        if user_role != required_role:
            return f"❌ Ошибка: Недостаточно прав. Требуется роль: {required_role}"
        
        print(f"✅ Права доступа проверены. Роль: {user_role}")
        return super().handle(request)


class ValidationHandler(Handler):
    """Обработчик валидации данных"""
    def handle(self, request: dict) -> Optional[str]:
        print("📋 Валидация данных...")
        
        data = request.get("data", {})
        
        if not data.get("email") or "@" not in data["email"]:
            return "❌ Ошибка: Некорректный email"
        
        if not data.get("age") or data["age"] < 18:
            return "❌ Ошибка: Пользователь должен быть старше 18 лет"
        
        print("✅ Данные валидны")
        return super().handle(request)


class LoggingHandler(Handler):
    """Обработчик логирования"""
    def handle(self, request: dict) -> Optional[str]:
        print("📝 Логирование запроса...")
        
     
        print(f"📋 Запрос успешно обработан:")
        print(f"   Пользователь: {request.get('username', 'Неизвестно')}")
        print(f"   Роль: {request.get('user_role', 'Неизвестно')}")
        print(f"   Данные: {request.get('data', {})}")
        
        return super().handle(request)


class SuccessHandler(Handler):
    """Финальный обработчик - успешное выполнение"""
    def handle(self, request: dict) -> Optional[str]:
        print("🎉 Выполнение основного действия...")
        
     
        data = request.get("data", {})
        print(f"✅ Действие успешно выполнено для {data.get('email', 'пользователя')}")
        
       
        return f"✅ Запрос успешно обработан для пользователя {request.get('username')}"



def process_request(request: dict) -> str:
    """Обработка запроса через цепочку"""
    print(f"\n🔍 Обрабатываем запрос от {request.get('username')}")
    print("-" * 40)
    
 
    auth = AuthHandler()
    permissions = PermissionHandler()
    validation = ValidationHandler()
    logging = LoggingHandler()
    success = SuccessHandler()
    

    auth.set_next(permissions).set_next(validation).set_next(logging).set_next(success)
    

    return auth.handle(request) or "Запрос не обработан"



if __name__ == "__main__":
    print("=== Паттерн Цепочка обязанностей (Chain of Responsibility) ===\n")
    
    
    print("Тест 1: Успешный запрос")
    request1 = {
        "username": "ivan_ivanov",
        "authenticated": True,
        "user_role": "admin",
        "required_role": "admin",
        "data": {
            "email": "ivan@example.com",
            "age": 25,
            "message": "Привет, мир!"
        }
    }
    
    result1 = process_request(request1)
    print(f"\nРезультат: {result1}")
    
    
    print("\n" + "="*50)
    print("Тест 2: Ошибка аутентификации")
    request2 = {
        "username": "guest",
        "authenticated": False,  
        "user_role": "guest",
        "required_role": "user",
        "data": {"email": "guest@example.com", "age": 20}
    }
    
    result2 = process_request(request2)
    print(f"\nРезультат: {result2}")
    
    
    print("\n" + "="*50)
    print("Тест 3: Недостаточно прав")
    request3 = {
        "username": "simple_user",
        "authenticated": True,
        "user_role": "user",  
        "required_role": "admin",  
        "data": {"email": "user@example.com", "age": 30}
    }
    
    result3 = process_request(request3)
    print(f"\nРезультат: {result3}")
    
   
    print("\n" + "="*50)
    print("Тест 4: Некорректные данные")
    request4 = {
        "username": "young_user",
        "authenticated": True,
        "user_role": "admin",
        "required_role": "admin",
        "data": {
            "email": "invalid-email",  
            "age": 16  
        }
    }
    
    result4 = process_request(request4)
    print(f"\nРезультат: {result4}")
    
    print("\n✅ Цепочка обязанностей работает корректно!")