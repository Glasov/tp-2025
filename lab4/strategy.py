"""
Паттерн Стратегия (Strategy)
Определяет семейство алгоритмов, инкапсулирует каждый из них и делает их взаимозаменяемыми.
"""

from abc import ABC, abstractmethod
from typing import List



class SortStrategy(ABC):
    """Абстрактная стратегия сортировки"""
    @abstractmethod
    def sort(self, data: List) -> List:
        pass


class BubbleSortStrategy(SortStrategy):
    """Конкретная стратегия: пузырьковая сортировка"""
    def sort(self, data: List) -> List:
        print("Сортируем пузырьком...")
        arr = data.copy()
        n = len(arr)
        for i in range(n-1):
            for j in range(n-i-1):
                if arr[j] > arr[j+1]:
                    arr[j], arr[j+1] = arr[j+1], arr[j]
        return arr


class QuickSortStrategy(SortStrategy):
    """Конкретная стратегия: быстрая сортировка"""
    def sort(self, data: List) -> List:
        print("Сортируем быстрой сортировкой...")
        return self._quick_sort(data.copy())
    
    def _quick_sort(self, arr):
        if len(arr) <= 1:
            return arr
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        return self._quick_sort(left) + middle + self._quick_sort(right)


class ReverseSortStrategy(SortStrategy):
    """Конкретная стратегия: обратная сортировка"""
    def sort(self, data: List) -> List:
        print("Сортируем в обратном порядке...")
        return sorted(data.copy(), reverse=True)



class Sorter:
    """Контекст, использующий стратегию"""
    def __init__(self, strategy: SortStrategy = None):
        self._strategy = strategy
    
    def set_strategy(self, strategy: SortStrategy):
        """Установка стратегии"""
        self._strategy = strategy
    
    def sort_data(self, data: List) -> List:
        """Выполнение сортировки с текущей стратегией"""
        if not self._strategy:
            raise ValueError("Стратегия не установлена!")
        return self._strategy.sort(data)


if __name__ == "__main__":
    print("=== Паттерн Стратегия (Strategy) ===\n")
    
    data = [64, 34, 25, 12, 22, 11, 90, 5]
    print(f"Исходные данные: {data}\n")
    
    sorter = Sorter()
    
  
    sorter.set_strategy(BubbleSortStrategy())
    result = sorter.sort_data(data)
    print(f"Результат: {result}\n")
    
    
    sorter.set_strategy(QuickSortStrategy())
    result = sorter.sort_data(data)
    print(f"Результат: {result}\n")
    
    
    sorter.set_strategy(ReverseSortStrategy())
    result = sorter.sort_data(data)
    print(f"Результат: {result}\n")
    
    print("✅ Стратегия работает корректно!")