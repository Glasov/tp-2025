"""
Паттерн Итератор (Iterator)
Предоставляет способ последовательного доступа к элементам составного объекта,
не раскрывая его внутреннего представления.
"""

from abc import ABC, abstractmethod
from typing import Any, List


class Iterator(ABC):
    """Абстрактный итератор"""
    @abstractmethod
    def __next__(self) -> Any:
        pass
    
    @abstractmethod
    def has_next(self) -> bool:
        pass


class Aggregate(ABC):
    """Абстрактный агрегатор (коллекция)"""
    @abstractmethod
    def create_iterator(self) -> Iterator:
        pass



class Book:
    """Книга - элемент коллекции"""
    def __init__(self, title: str, author: str, year: int):
        self.title = title
        self.author = author
        self.year = year
    
    def __str__(self) -> str:
        return f"'{self.title}' - {self.author} ({self.year})"


class BookShelf(Aggregate):
    """Книжная полка - конкретная коллекция"""
    def __init__(self):
        self._books: List[Book] = []
    
    def add_book(self, book: Book) -> None:
        """Добавить книгу на полку"""
        self._books.append(book)
    
    def remove_book(self, book: Book) -> None:
        """Убрать книгу с полки"""
        if book in self._books:
            self._books.remove(book)
    
    def get_book_at(self, index: int) -> Book:
        """Получить книгу по индексу"""
        if 0 <= index < len(self._books):
            return self._books[index]
        raise IndexError("Неверный индекс")
    
    def get_count(self) -> int:
        """Количество книг на полке"""
        return len(self._books)
    
    def create_iterator(self) -> Iterator:
        """Создать итератор для обхода книг"""
        return BookShelfIterator(self)



class BookShelfIterator(Iterator):
    """Итератор для книжной полки"""
    def __init__(self, book_shelf: BookShelf):
        self._book_shelf = book_shelf
        self._index = 0
    
    def __next__(self) -> Book:
        """Получить следующую книгу"""
        if not self.has_next():
            raise StopIteration("Книги закончились")
        
        book = self._book_shelf.get_book_at(self._index)
        self._index += 1
        return book
    
    def has_next(self) -> bool:
        """Проверить, есть ли следующая книга"""
        return self._index < self._book_shelf.get_count()



class ReverseBookShelfIterator(Iterator):
    """Обратный итератор для книжной полки"""
    def __init__(self, book_shelf: BookShelf):
        self._book_shelf = book_shelf
        self._index = book_shelf.get_count() - 1
    
    def __next__(self) -> Book:
        """Получить предыдущую книгу"""
        if not self.has_next():
            raise StopIteration("Книги закончились")
        
        book = self._book_shelf.get_book_at(self._index)
        self._index -= 1
        return book
    
    def has_next(self) -> bool:
        """Проверить, есть ли предыдущая книга"""
        return self._index >= 0


class AuthorFilterIterator(Iterator):
    """Итератор с фильтром по автору"""
    def __init__(self, book_shelf: BookShelf, author: str):
        self._book_shelf = book_shelf
        self._author = author.lower()
        self._index = 0
        self._find_next()
    
    def _find_next(self) -> None:
        """Найти следующую книгу указанного автора"""
        while self._index < self._book_shelf.get_count():
            book = self._book_shelf.get_book_at(self._index)
            if book.author.lower() == self._author:
                break
            self._index += 1
    
    def __next__(self) -> Book:
        """Получить следующую книгу указанного автора"""
        if not self.has_next():
            raise StopIteration(f"Книги автора '{self._author}' закончились")
        
        book = self._book_shelf.get_book_at(self._index)
        self._index += 1
        self._find_next()
        return book
    
    def has_next(self) -> bool:
        """Проверить, есть ли следующая книга указанного автора"""
        return self._index < self._book_shelf.get_count()



if __name__ == "__main__":
    print("=== Паттерн Итератор (Iterator) ===\n")
    
  
    shelf = BookShelf()
    
    
    books_data = [
        ("Война и мир", "Лев Толстой", 1869),
        ("Преступление и наказание", "Фёдор Достоевский", 1866),
        ("Мастер и Маргарита", "Михаил Булгаков", 1967),
        ("Анна Каренина", "Лев Толстой", 1877),
        ("Идиот", "Фёдор Достоевский", 1869),
        ("Собачье сердце", "Михаил Булгаков", 1925),
        ("Воскресение", "Лев Толстой", 1899),
    ]
    
    for title, author, year in books_data:
        shelf.add_book(Book(title, author, year))
    
    print(f"📚 На полке {shelf.get_count()} книг\n")
    
 
    print("1. Обычный обход книг:")
    print("-" * 40)
    iterator = shelf.create_iterator()
    
    while iterator.has_next():
        book = next(iterator)
        print(f"  • {book}")
    
    print("\n2. Обход через for-in (встроенная поддержка):")
    print("-" * 40)
   
    iterator = shelf.create_iterator()
    for book in iter(iterator.__next__, None):
        print(f"  • {book}")
    
   
    print("\n3. Обратный обход книг:")
    print("-" * 40)
    reverse_iterator = ReverseBookShelfIterator(shelf)
    
    while reverse_iterator.has_next():
        book = next(reverse_iterator)
        print(f"  • {book}")
    
    
    print("\n4. Книги Льва Толстого (фильтр по автору):")
    print("-" * 40)
    tolstoii_iterator = AuthorFilterIterator(shelf, "Лев Толстой")
    
    while tolstoii_iterator.has_next():
        book = next(tolstoii_iterator)
        print(f"  • {book}")
    
    
    print("\n5. Несколько итераторов работают независимо:")
    print("-" * 40)
    
    iterator1 = shelf.create_iterator()
    iterator2 = shelf.create_iterator()
    
    print("Итератор 1 (первые 2 книги):")
    for _ in range(2):
        if iterator1.has_next():
            print(f"  • {next(iterator1)}")
    
    print("\nИтератор 2 (все книги):")
    while iterator2.has_next():
        print(f"  • {next(iterator2)}")
    
    print("\nИтератор 1 (продолжение):")
    while iterator1.has_next():
        print(f"  • {next(iterator1)}")
    
    
    print("\n6. Обработка пустой коллекции:")
    print("-" * 40)
    empty_shelf = BookShelf()
    empty_iterator = empty_shelf.create_iterator()
    
    if not empty_iterator.has_next():
        print("  Полка пуста - нечего перебирать")
    
    print("\n✅ Итератор работает корректно!")