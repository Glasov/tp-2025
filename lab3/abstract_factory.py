from abc import ABC, abstractmethod


class Button(ABC):
    """Абстрактная кнопка"""
    @abstractmethod
    def paint(self) -> str:
        pass


class Checkbox(ABC):
    """Абстрактный чекбокс"""
    @abstractmethod
    def paint(self) -> str:
        pass


class Scrollbar(ABC):
    """Абстрактный скроллбар"""
    @abstractmethod
    def paint(self) -> str:
        pass



class WindowsButton(Button):
    def paint(self) -> str:
        return "🪟 Отрисована кнопка в стиле Windows"


class WindowsCheckbox(Checkbox):
    def paint(self) -> str:
        return "✅ Отрисован чекбокс в стиле Windows"


class WindowsScrollbar(Scrollbar):
    def paint(self) -> str:
        return "📏 Отрисован скроллбар в стиле Windows"



class MacButton(Button):
    def paint(self) -> str:
        return "🍎 Отрисована кнопка в стиле macOS"


class MacCheckbox(Checkbox):
    def paint(self) -> str:
        return "☑️ Отрисован чекбокс в стиле macOS"


class MacScrollbar(Scrollbar):
    def paint(self) -> str:
        return "🧭 Отрисован скроллбар в стиле macOS"



class LinuxButton(Button):
    def paint(self) -> str:
        return "🐧 Отрисована кнопка в стиле Linux"


class LinuxCheckbox(Checkbox):
    def paint(self) -> str:
        return "✓ Отрисован чекбокс в стиле Linux"


class LinuxScrollbar(Scrollbar):
    def paint(self) -> str:
        return "↕️ Отрисован скроллбар в стиле Linux"



class GUIFactory(ABC):
    """Абстрактная фабрика GUI элементов"""
    @abstractmethod
    def create_button(self) -> Button:
        pass
    
    @abstractmethod
    def create_checkbox(self) -> Checkbox:
        pass
    
    @abstractmethod
    def create_scrollbar(self) -> Scrollbar:
        pass



class WindowsFactory(GUIFactory):
    """Фабрика для создания Windows-стиля элементов"""
    def create_button(self) -> Button:
        return WindowsButton()
    
    def create_checkbox(self) -> Checkbox:
        return WindowsCheckbox()
    
    def create_scrollbar(self) -> Scrollbar:
        return WindowsScrollbar()


class MacFactory(GUIFactory):
    """Фабрика для создания macOS-стиля элементов"""
    def create_button(self) -> Button:
        return MacButton()
    
    def create_checkbox(self) -> Checkbox:
        return MacCheckbox()
    
    def create_scrollbar(self) -> Scrollbar:
        return MacScrollbar()


class LinuxFactory(GUIFactory):
    """Фабрика для создания Linux-стиля элементов"""
    def create_button(self) -> Button:
        return LinuxButton()
    
    def create_checkbox(self) -> Checkbox:
        return LinuxCheckbox()
    
    def create_scrollbar(self) -> Scrollbar:
        return LinuxScrollbar()



class Application:
    """Приложение, которое использует GUI элементы"""
    def __init__(self, factory: GUIFactory):
        self.factory = factory
        self.button = None
        self.checkbox = None
        self.scrollbar = None
    
    def create_ui(self):
        """Создаёт все UI элементы через фабрику"""
        self.button = self.factory.create_button()
        self.checkbox = self.factory.create_checkbox()
        self.scrollbar = self.factory.create_scrollbar()
    
    def paint_ui(self):
        """Отрисовывает все UI элементы"""
        if self.button and self.checkbox and self.scrollbar:
            print("🎨 Отрисовываем интерфейс:")
            print(f"  - {self.button.paint()}")
            print(f"  - {self.checkbox.paint()}")
            print(f"  - {self.scrollbar.paint()}")
        else:
            print("❌ Сначала создайте UI!")



if __name__ == "__main__":
    print("=== Тест паттерна Abstract Factory ===\n")
    
   
    
    os_factories = {
        "Windows": WindowsFactory(),
        "macOS": MacFactory(),
        "Linux": LinuxFactory()
    }
    
   
    for os_name, factory in os_factories.items():
        print(f"\n--- Создаём приложение для {os_name} ---")
        app = Application(factory)
        app.create_ui()
        app.paint_ui()
    
   
    print("\n=== Важность консистентности стиля ===")
    print("Все элементы созданы одной фабрикой → все в одном стиле!")
    print("Нельзя смешать Windows-кнопку с macOS-чекбоксом через одну фабрику.")
    
    
    print("\n=== Конфигурирование фабрики ===")
    config = "Windows"  
    print(f"Конфигурация: {config}")
    
    if config == "Windows":
        factory = WindowsFactory()
    elif config == "macOS":
        factory = MacFactory()
    else:
        factory = LinuxFactory()
    
    app = Application(factory)
    app.create_ui()
    app.paint_ui()
    
    print("\n✅ Abstract Factory работает корректно!")