"""
Паттерн Прокси (Proxy)
Предоставляет объект-заместитель, который контролирует доступ к другому объекту.
"""

from abc import ABC, abstractmethod
import time
from typing import Optional



class Database(ABC):
    """Абстрактный субъект - база данных"""
    @abstractmethod
    def execute_query(self, query: str) -> str:
        pass
    
    @abstractmethod
    def get_connection_info(self) -> dict:
        pass


class RealDatabase(Database):
    """Реальная база данных (тяжелый объект)"""
    def __init__(self, host: str, port: int):
        print(f"⏳ Инициализация подключения к базе данных {host}:{port}...")
        time.sleep(2)  
        self._host = host
        self._port = port
        self._connected = True
        print("✅ Подключение к базе данных установлено")
    
    def execute_query(self, query: str) -> str:
        """Выполнение SQL-запроса"""
        if not self._connected:
            raise ConnectionError("База данных не подключена")
        
        print(f"📊 Выполняем запрос: {query}")
        time.sleep(1) 
        
  
        if "SELECT" in query.upper():
            return f"Результаты запроса: 100 записей найдено"
        elif "INSERT" in query.upper():
            return "Запись успешно добавлена"
        elif "DELETE" in query.upper():
            return "Запись успешно удалена"
        else:
            return "Запрос выполнен успешно"
    
    def get_connection_info(self) -> dict:
        """Получить информацию о подключении"""
        return {
            "host": self._host,
            "port": self._port,
            "status": "connected" if self._connected else "disconnected"
        }
    
    def close(self):
        """Закрыть подключение"""
        print("🔌 Закрываем подключение к базе данных...")
        self._connected = False



class DatabaseProxy(Database):
    """Прокси для базы данных с ленивой инициализацией и кэшированием"""
    def __init__(self, host: str, port: int):
        self._host = host
        self._port = port
        self._real_database: Optional[RealDatabase] = None
        self._cache = {} 
        self._access_count = 0
        self._max_cache_size = 3
    
    def _initialize_database(self) -> None:
        """Ленивая инициализация реальной базы данных"""
        if self._real_database is None:
            self._real_database = RealDatabase(self._host, self._port)
    
    def execute_query(self, query: str) -> str:
        """Выполнение запроса с кэшированием и контролем доступа"""
        self._access_count += 1
        print(f"\n📝 Запрос #{self._access_count}: {query}")
        
     
        if not self._check_access(query):
            return "❌ Ошибка: Недостаточно прав для выполнения этого запроса"
        
        
        if query in self._cache:
            print("⚡ Используем кэшированный результат")
            return self._cache[query]
        
       
        self._initialize_database()
        
     
        result = self._real_database.execute_query(query)
        
      
        self._cache[query] = result
        print(f"💾 Результат закэширован")
        
    
        if len(self._cache) > self._max_cache_size:
            oldest_query = next(iter(self._cache))
            del self._cache[oldest_query]
            print(f"🧹 Удален из кэша: {oldest_query[:30]}...")
        
        return result
    
    def get_connection_info(self) -> dict:
        """Получить информацию о подключении (без инициализации реальной БД)"""
        if self._real_database:
            info = self._real_database.get_connection_info()
        else:
            info = {
                "host": self._host,
                "port": self._port,
                "status": "not_initialized"
            }
        
        info["cache_size"] = len(self._cache)
        info["access_count"] = self._access_count
        return info
    
    def _check_access(self, query: str) -> bool:
        """Проверка прав доступа к запросу"""
        
        restricted_keywords = ["DROP", "DELETE", "TRUNCATE"]
        query_upper = query.upper()
        
        for keyword in restricted_keywords:
            if keyword in query_upper:
                print(f"⚠️  Обнаружена потенциально опасная операция: {keyword}")
             
                return False
        
        return True
    
    def clear_cache(self):
        """Очистить кэш"""
        self._cache.clear()
        print("🧹 Кэш очищен")
    
    def get_cache_stats(self) -> dict:
        """Статистика кэша"""
        return {
            "cached_queries": list(self._cache.keys()),
            "cache_size": len(self._cache),
            "access_count": self._access_count
        }


class ProtectedDatabaseProxy(Database):
    """Защищающий прокси с аутентификацией"""
    def __init__(self, real_database: Database, username: str, password: str):
        self._real_database = real_database
        self._username = username
        self._password = password
        self._authenticated = False
    
    def authenticate(self, username: str, password: str) -> bool:
        """Аутентификация пользователя"""
        if username == self._username and password == self._password:
            self._authenticated = True
            print(f"✅ Пользователь {username} успешно аутентифицирован")
            return True
        
        print(f"❌ Ошибка аутентификации для пользователя {username}")
        return False
    
    def execute_query(self, query: str) -> str:
        """Выполнение запроса с проверкой аутентификации"""
        if not self._authenticated:
            return "❌ Ошибка: Требуется аутентификация. Вызовите authenticate()"
        
  
        if self._is_admin_query(query) and self._username != "admin":
            return "❌ Ошибка: Только администратор может выполнять этот запрос"
        
        return self._real_database.execute_query(query)
    
    def get_connection_info(self) -> dict:
        """Получить информацию о подключении"""
        info = self._real_database.get_connection_info()
        info["user"] = self._username
        info["authenticated"] = self._authenticated
        return info
    
    def _is_admin_query(self, query: str) -> bool:
        """Проверка, является ли запрос административным"""
        admin_keywords = ["CREATE", "DROP", "ALTER", "GRANT", "REVOKE"]
        query_upper = query.upper()
        
        for keyword in admin_keywords:
            if keyword in query_upper:
                return True
        
        return False



if __name__ == "__main__":
    print("=== Паттерн Прокси (Proxy) ===\n")
    
  
    print("1. Прокси с ленивой инициализацией и кэшированием:")
    print("=" * 60)
    
    proxy = DatabaseProxy("localhost", 5432)
    
   
    print(f"Информация до инициализации: {proxy.get_connection_info()}")
    
    
    print("\nПервый запрос (SELECT):")
    result1 = proxy.execute_query("SELECT * FROM users WHERE age > 18")
    print(f"Результат: {result1}")
    
    
    print("\nТот же запрос (должен быть из кэша):")
    result2 = proxy.execute_query("SELECT * FROM users WHERE age > 18")
    print(f"Результат: {result2}")
    
    
    print("\nНовый запрос (INSERT):")
    result3 = proxy.execute_query("INSERT INTO users VALUES ('John', 25)")
    print(f"Результат: {result3}")
    
    
    print("\nОпасный запрос (DROP):")
    result4 = proxy.execute_query("DROP TABLE users")
    print(f"Результат: {result4}")
    
   
    print(f"\nСтатистика прокси: {proxy.get_cache_stats()}")
    
   
    print("\n\n2. Защищающий прокси с аутентификацией:")
    print("=" * 60)
    
    
    real_db = RealDatabase("db.example.com", 3306)
    
   
    protected_proxy = ProtectedDatabaseProxy(real_db, "admin", "secret123")
    
    
    print("\nПопытка выполнить запрос без аутентификации:")
    result5 = protected_proxy.execute_query("SELECT * FROM products")
    print(f"Результат: {result5}")
    
    
    print("\nАутентификация с неправильным паролем:")
    protected_proxy.authenticate("admin", "wrongpassword")
    
   
    print("\nАутентификация с правильным паролем:")
    protected_proxy.authenticate("admin", "secret123")
    
   
    print("\nВыполнение запроса после аутентификации:")
    result6 = protected_proxy.execute_query("SELECT * FROM products")
    print(f"Результат: {result6}")
    
   
    print("\nСоздаем прокси для обычного пользователя:")
    user_proxy = ProtectedDatabaseProxy(real_db, "user", "user123")
    user_proxy.authenticate("user", "user123")
    
    print("Попытка выполнить административный запрос:")
    result7 = user_proxy.execute_query("CREATE TABLE test (id INT)")
    print(f"Результат: {result7}")
    
    
    print("\n\n3. Прозрачность использования (клиент не знает о прокси):")
    print("=" * 60)
    
    def process_database_operations(database: Database):
        """Функция, которая работает с любым объектом Database"""
        print(f"\nИнформация о подключении: {database.get_connection_info()}")
        
        queries = [
            "SELECT * FROM orders",
            "UPDATE products SET price = price * 1.1",
            "SELECT * FROM orders"  
        ]
        
        for query in queries:
            result = database.execute_query(query)
            print(f"Запрос: {query[:30]}... -> {result[:50]}...")
    
    print("\nРабота с реальной базой данных:")
    process_database_operations(real_db)
    
    print("\nРабота с прокси (тот же интерфейс):")
    process_database_operations(proxy)
    
    print("\n✅ Прокси работает корректно!")