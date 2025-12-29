from abc import ABC, abstractmethod
from typing import List, Optional

# ============================
# 1. Продукт - Сложный объект
# ============================
class Computer:
    """Сложный объект - компьютер"""
    def __init__(self):
        self.cpu: Optional[str] = None
        self.ram: Optional[str] = None
        self.storage: Optional[str] = None
        self.gpu: Optional[str] = None
        self.psu: Optional[str] = None
        self.cooling: Optional[str] = None
        self.extras: List[str] = []
    
    def __str__(self) -> str:
        parts = [
            f"💻 Компьютерная сборка:",
            f"  Процессор: {self.cpu or 'Не установлен'}",
            f"  Оперативная память: {self.ram or 'Не установлена'}",
            f"  Накопитель: {self.storage or 'Не установлен'}",
            f"  Видеокарта: {self.gpu or 'Не установлена'}",
            f"  Блок питания: {self.psu or 'Не установлен'}",
            f"  Охлаждение: {self.cooling or 'Не установлено'}"
        ]
        
        if self.extras:
            parts.append("  Дополнительно:")
            for extra in self.extras:
                parts.append(f"    • {extra}")
        
        return "\n".join(parts)
    
    def specifications(self) -> dict:
        """Возвращает спецификации в виде словаря"""
        return {
            "CPU": self.cpu,
            "RAM": self.ram,
            "Storage": self.storage,
            "GPU": self.gpu,
            "PSU": self.psu,
            "Cooling": self.cooling,
            "Extras": self.extras
        }


# ============================
# 2. Абстрактный строитель
# ============================
class ComputerBuilder(ABC):
    """Абстрактный строитель компьютеров"""
    def __init__(self):
        self.reset()
    
    def reset(self):
        """Сбрасывает строителя для новой сборки"""
        self._computer = Computer()
    
    @property
    def computer(self) -> Computer:
        """Возвращает готовый компьютер"""
        computer = self._computer
        self.reset()  # Готовим строителя к следующей сборке
        return computer
    
    @abstractmethod
    def set_cpu(self) -> None:
        pass
    
    @abstractmethod
    def set_ram(self) -> None:
        pass
    
    @abstractmethod
    def set_storage(self) -> None:
        pass
    
    @abstractmethod
    def set_gpu(self) -> None:
        pass
    
    @abstractmethod
    def set_psu(self) -> None:
        pass
    
    @abstractmethod
    def set_cooling(self) -> None:
        pass
    
    def add_extra(self, extra: str) -> None:
        """Добавляет дополнительный компонент (опциональный метод)"""
        self._computer.extras.append(extra)


# ============================
# 3. Конкретные строители
# ============================
class GamingComputerBuilder(ComputerBuilder):
    """Строитель игровых компьютеров"""
    def set_cpu(self) -> None:
        self._computer.cpu = "Intel Core i9-14900K"
    
    def set_ram(self) -> None:
        self._computer.ram = "64GB DDR5 6000MHz"
    
    def set_storage(self) -> None:
        self._computer.storage = "2TB NVMe SSD + 4TB HDD"
    
    def set_gpu(self) -> None:
        self._computer.gpu = "NVIDIA RTX 4090 24GB"
    
    def set_psu(self) -> None:
        self._computer.psu = "1200W 80+ Platinum"
    
    def set_cooling(self) -> None:
        self._computer.cooling = "Жидкостное охлаждение с RGB"


class OfficeComputerBuilder(ComputerBuilder):
    """Строитель офисных компьютеров"""
    def set_cpu(self) -> None:
        self._computer.cpu = "Intel Core i5-13400"
    
    def set_ram(self) -> None:
        self._computer.ram = "16GB DDR4 3200MHz"
    
    def set_storage(self) -> None:
        self._computer.storage = "512GB NVMe SSD"
    
    def set_gpu(self) -> None:
        self._computer.gpu = "Интегрированная графика"
    
    def set_psu(self) -> None:
        self._computer.psu = "500W 80+ Bronze"
    
    def set_cooling(self) -> None:
        self._computer.cooling = "Воздушное охлаждение"


class ServerComputerBuilder(ComputerBuilder):
    """Строитель серверных компьютеров"""
    def set_cpu(self) -> None:
        self._computer.cpu = "AMD EPYC 9654 (96 ядер)"
    
    def set_ram(self) -> None:
        self._computer.ram = "256GB DDR5 ECC"
    
    def set_storage(self) -> None:
        self._computer.storage = "8TB NVMe SSD RAID 10"
    
    def set_gpu(self) -> None:
        self._computer.gpu = "Без дискретной видеокарты"
    
    def set_psu(self) -> None:
        self._computer.psu = "1600W Dual PSU Redundant"
    
    def set_cooling(self) -> None:
        self._computer.cooling = "Пассивное охлаждение с дублированием"


# ============================
# 4. Директор (опционально)
# ============================
class ComputerAssembler:
    """Директор - управляет процессом сборки"""
    def __init__(self):
        self._builder: Optional[ComputerBuilder] = None
    
    @property
    def builder(self) -> ComputerBuilder:
        return self._builder
    
    @builder.setter
    def builder(self, builder: ComputerBuilder):
        self._builder = builder
    
    def build_basic_computer(self):
        """Собирает базовый компьютер (без дополнений)"""
        if not self._builder:
            raise ValueError("Сначала установите строителя!")
        
        self._builder.set_cpu()
        self._builder.set_ram()
        self._builder.set_storage()
        self._builder.set_gpu()
        self._builder.set_psu()
        self._builder.set_cooling()
        
        return self._builder.computer
    
    def build_premium_computer(self):
        """Собирает премиум компьютер с дополнениями"""
        if not self._builder:
            raise ValueError("Сначала установите строителя!")
        
        self._builder.set_cpu()
        self._builder.set_ram()
        self._builder.set_storage()
        self._builder.set_gpu()
        self._builder.set_psu()
        self._builder.set_cooling()
        
        # Добавляем премиум функции
        self._builder.add_extra("RGB подсветка корпуса")
        self._builder.add_extra("Кастомные кабели")
        self._builder.add_extra("Дополнительные вентиляторы")
        self._builder.add_extra("Гарантия 5 лет")
        
        return self._builder.computer


# ============================
# 5. Тестирование
# ============================
if __name__ == "__main__":
    print("=== Тест паттерна Builder ===\n")
    
    # ============================
    # Способ 1: Использование напрямую
    # ============================
    print("1. Прямое использование строителя:")
    print("-" * 40)
    
    gaming_builder = GamingComputerBuilder()
    
    # Пошаговая сборка
    gaming_builder.set_cpu()
    gaming_builder.set_ram()
    gaming_builder.set_storage()
    gaming_builder.set_gpu()
    gaming_builder.set_psu()
    gaming_builder.set_cooling()
    
    # Добавляем дополнения
    gaming_builder.add_extra("Игровая мышь")
    gaming_builder.add_extra("Механическая клавиатура")
    
    gaming_pc = gaming_builder.computer
    print(gaming_pc)
    print()
    
    # ============================
    # Способ 2: Использование с директором
    # ============================
    print("2. Использование с директором:")
    print("-" * 40)
    
    assembler = ComputerAssembler()
    
    # Собираем офисный компьютер
    print("Сборка офисного компьютера:")
    office_builder = OfficeComputerBuilder()
    assembler.builder = office_builder
    office_pc = assembler.build_basic_computer()
    print(office_pc)
    print()
    
    # Собираем серверный компьютер
    print("Сборка серверного компьютера:")
    server_builder = ServerComputerBuilder()
    assembler.builder = server_builder
    server_pc = assembler.build_premium_computer()
    print(server_pc)
    print()
    
    # ============================
    # Способ 3: Кастомная сборка
    # ============================
    print("3. Кастомная сборка (без директора):")
    print("-" * 40)
    
    class CustomComputerBuilder(ComputerBuilder):
        """Строитель для кастомной сборки"""
        def set_cpu(self) -> None:
            self._computer.cpu = "AMD Ryzen 7 7800X3D"
        
        def set_ram(self) -> None:
            self._computer.ram = "32GB DDR5 5600MHz"
        
        def set_storage(self) -> None:
            self._computer.storage = "1TB NVMe SSD"
        
        def set_gpu(self) -> None:
            self._computer.gpu = "AMD Radeon RX 7900 XTX"
        
        def set_psu(self) -> None:
            self._computer.psu = "850W 80+ Gold"
        
        def set_cooling(self) -> None:
            self._computer.cooling = "Кастомный жидкостный контур"
    
    custom_builder = CustomComputerBuilder()
    
    # Собираем только нужные части
    custom_builder.set_cpu()
    custom_builder.set_ram()
    custom_builder.set_storage()
    # Не устанавливаем GPU - будет по умолчанию
    custom_builder.set_psu()
    custom_builder.set_cooling()
    
    custom_pc = custom_builder.computer
    print(custom_pc)
    print()
    
    # ============================
    # Преимущества паттерна
    # ============================
    print("=== Преимущества паттерна Builder ===")
    print("1. Пошаговое создание сложных объектов")
    print("2. Один и тот же код может создавать разные представления")
    print("3. Изоляция сложного кода сборки")
    print("4. Легко добавлять новые виды сборок")
    print("5. Возможность создания 'полуфабрикатов' (объектов без всех частей)")
    
    print("\n✅ Builder работает корректно!")