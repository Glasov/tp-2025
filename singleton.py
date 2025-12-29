class DatabaseConnection:
    """
    Класс, реализующий паттерн Singleton.
    Гарантирует, что существует только один экземпляр этого класса.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            print("Создаём новое подключение к базе данных...")
            cls._instance = super().__new__(cls)
            cls._instance.connection = "Активное подключение к БД"
        else:
            print("Используем существующее подключение...")
        return cls._instance

    def query(self, sql: str) -> str:
        """Выполняет SQL-запрос"""
        return f"Выполняем запрос: '{sql}'"

# Тестирование
if __name__ == "__main__":
    print("=== Тест паттерна Singleton ===\n")

    # Пытаемся создать два "разных" объекта
    db1 = DatabaseConnection()
    db2 = DatabaseConnection()

    print(f"\ndb1 is db2? {db1 is db2}")  # Должно быть True
    print(f"ID db1: {id(db1)}")
    print(f"ID db2: {id(db2)}")

    # Проверяем, что это действительно один и тот же объект
    print(f"\ndb1.connection: {db1.connection}")
    print(f"db2.connection: {db2.connection}")

    # Выполняем запрос
    print(f"\n{db1.query('SELECT * FROM users')}")
    print(f"{db2.query('DROP TABLE users')}")

    print("\n✅ Singleton работает корректно!")