"""
Паттерн Мост (Bridge)
Разделяет абстракцию и реализацию так, чтобы они могли изменяться независимо.
"""

from abc import ABC, abstractmethod
from typing import List



class Device(ABC):
    """Абстракция реализации - устройство"""
    @abstractmethod
    def is_enabled(self) -> bool:
        pass
    
    @abstractmethod
    def enable(self) -> None:
        pass
    
    @abstractmethod
    def disable(self) -> None:
        pass
    
    @abstractmethod
    def get_volume(self) -> int:
        pass
    
    @abstractmethod
    def set_volume(self, percent: int) -> None:
        pass
    
    @abstractmethod
    def get_channel(self) -> int:
        pass
    
    @abstractmethod
    def set_channel(self, channel: int) -> None:
        pass
    
    @abstractmethod
    def print_status(self) -> None:
        pass


class TV(Device):
    """Конкретная реализация - телевизор"""
    def __init__(self):
        self._enabled = False
        self._volume = 20
        self._channel = 1
        self._max_channel = 100
    
    def is_enabled(self) -> bool:
        return self._enabled
    
    def enable(self) -> None:
        self._enabled = True
        print("📺 Телевизор включен")
    
    def disable(self) -> None:
        self._enabled = False
        print("📺 Телевизор выключен")
    
    def get_volume(self) -> int:
        return self._volume
    
    def set_volume(self, percent: int) -> None:
        if 0 <= percent <= 100:
            self._volume = percent
            print(f"📺 Громкость телевизора: {percent}%")
        else:
            print("❌ Громкость должна быть от 0 до 100%")
    
    def get_channel(self) -> int:
        return self._channel
    
    def set_channel(self, channel: int) -> None:
        if 1 <= channel <= self._max_channel:
            self._channel = channel
            print(f"📺 Канал телевизора: {channel}")
        else:
            print(f"❌ Канал должен быть от 1 до {self._max_channel}")
    
    def print_status(self) -> None:
        status = "включен" if self._enabled else "выключен"
        print(f"📺 Телевизор: {status}, громкость: {self._volume}%, канал: {self._channel}")


class Radio(Device):
    """Конкретная реализация - радио"""
    def __init__(self):
        self._enabled = False
        self._volume = 30
        self._channel = 88.5  
        self._min_freq = 87.5
        self._max_freq = 108.0
    
    def is_enabled(self) -> bool:
        return self._enabled
    
    def enable(self) -> None:
        self._enabled = True
        print("📻 Радио включено")
    
    def disable(self) -> None:
        self._enabled = False
        print("📻 Радио выключено")
    
    def get_volume(self) -> int:
        return self._volume
    
    def set_volume(self, percent: int) -> None:
        if 0 <= percent <= 100:
            self._volume = percent
            print(f"📻 Громкость радио: {percent}%")
        else:
            print("❌ Громкость должна быть от 0 до 100%")
    
    def get_channel(self) -> float:
        return self._channel
    
    def set_channel(self, channel: float) -> None:
        if self._min_freq <= channel <= self._max_freq:
            self._channel = channel
            print(f"📻 Частота радио: {channel} FM")
        else:
            print(f"❌ Частота должна быть от {self._min_freq} до {self._max_freq} FM")
    
    def print_status(self) -> None:
        status = "включено" if self._enabled else "выключено"
        print(f"📻 Радио: {status}, громкость: {self._volume}%, частота: {self._channel} FM")



class RemoteControl(ABC):
    """Абстракция - пульт управления"""
    def __init__(self, device: Device):
        self._device = device
    
    def toggle_power(self) -> None:
        """Включить/выключить устройство"""
        if self._device.is_enabled():
            self._device.disable()
        else:
            self._device.enable()
    
    def volume_down(self) -> None:
        """Уменьшить громкость"""
        current = self._device.get_volume()
        self._device.set_volume(max(0, current - 10))
    
    def volume_up(self) -> None:
        """Увеличить громкость"""
        current = self._device.get_volume()
        self._device.set_volume(min(100, current + 10))
    
    def channel_down(self) -> None:
        """Перейти на предыдущий канал"""
        current = self._device.get_channel()
        self._device.set_channel(current - 1)
    
    def channel_up(self) -> None:
        """Перейти на следующий канал"""
        current = self._device.get_channel()
        self._device.set_channel(current + 1)
    
    @abstractmethod
    def special_feature(self) -> None:
        """Специальная функция пульта"""
        pass
    
    def print_status(self) -> None:
        """Показать статус устройства"""
        self._device.print_status()


class BasicRemote(RemoteControl):
    """Конкретная абстракция - базовый пульт"""
    def special_feature(self) -> None:
        print("📟 Базовый пульт: специальных функций нет")


class AdvancedRemote(RemoteControl):
    """Конкретная абстракция - продвинутый пульт"""
    def __init__(self, device: Device):
        super().__init__(device)
        self._muted = False
        self._previous_volume = 0
    
    def special_feature(self) -> None:
        """Специальная функция - mute"""
        if not self._muted:
            self._previous_volume = self._device.get_volume()
            self._device.set_volume(0)
            self._muted = True
            print("🔇 Звук отключен")
        else:
            self._device.set_volume(self._previous_volume)
            self._muted = False
            print(f"🔊 Звук включен: {self._previous_volume}%")
    
    def set_favorite_channel(self, channel: float) -> None:
        """Установить любимый канал"""
        self._device.set_channel(channel)
        print(f"⭐ Любимый канал установлен: {channel}")


class VoiceRemote(RemoteControl):
    """Конкретная абстракция - голосовой пульт"""
    def special_feature(self) -> None:
        print("🎤 Голосовой пульт: 'Скажите команду...'")
    
    def voice_command(self, command: str) -> None:
        """Обработка голосовой команды"""
        command = command.lower()
        
        if "включи" in command:
            if not self._device.is_enabled():
                self._device.enable()
        elif "выключи" in command:
            if self._device.is_enabled():
                self._device.disable()
        elif "громче" in command:
            self.volume_up()
        elif "тише" in command:
            self.volume_down()
        elif "канал" in command:
          
            for word in command.split():
                if word.isdigit():
                    self._device.set_channel(int(word))
                    break
        else:
            print(f"🤖 Не понял команду: {command}")



class SmartTV(Device):
    """Умный телевизор с дополнительными функциями"""
    def __init__(self):
        self._enabled = False
        self._volume = 15
        self._channel = 1
        self._apps = ["YouTube", "Netflix", "Browser"]
        self._current_app = None
        self._brightness = 50
    
    def is_enabled(self) -> bool:
        return self._enabled
    
    def enable(self) -> None:
        self._enabled = True
        print("📱 Умный телевизор включен")
    
    def disable(self) -> None:
        self._enabled = False
        self._current_app = None
        print("📱 Умный телевизор выключен")
    
    def get_volume(self) -> int:
        return self._volume
    
    def set_volume(self, percent: int) -> None:
        if 0 <= percent <= 100:
            self._volume = percent
            print(f"📱 Громкость умного ТВ: {percent}%")
    
    def get_channel(self) -> int:
        return self._channel
    
    def set_channel(self, channel: int) -> None:
        if channel >= 1:
            self._channel = channel
            print(f"📱 Канал умного ТВ: {channel}")
    
    def launch_app(self, app_name: str) -> None:
        """Запустить приложение (уникальная функция SmartTV)"""
        if app_name in self._apps:
            self._current_app = app_name
            print(f"📱 Запущено приложение: {app_name}")
        else:
            print(f"❌ Приложение {app_name} не найдено")
    
    def set_brightness(self, level: int) -> None:
        """Установить яркость (уникальная функция SmartTV)"""
        if 0 <= level <= 100:
            self._brightness = level
            print(f"📱 Яркость установлена: {level}%")
    
    def print_status(self) -> None:
        status = "включен" if self._enabled else "выключен"
        app_info = f", приложение: {self._current_app}" if self._current_app else ""
        print(f"📱 Умный ТВ: {status}, громкость: {self._volume}%, канал: {self._channel}{app_info}")



class SmartRemote(RemoteControl):
    """Умный пульт для SmartTV"""
    def special_feature(self) -> None:
        print("📱 Умный пульт: доступ к приложениям")
    
    def launch_app(self, app_name: str) -> None:
        """Запустить приложение на SmartTV"""
        if isinstance(self._device, SmartTV):
            self._device.launch_app(app_name)
        else:
            print("❌ Эта функция доступна только для SmartTV")
    
    def set_brightness(self, level: int) -> None:
        """Установить яркость на SmartTV"""
        if isinstance(self._device, SmartTV):
            self._device.set_brightness(level)
        else:
            print("❌ Эта функция доступна только для SmartTV")



if __name__ == "__main__":
    print("=== Паттерн Мост (Bridge) ===\n")
    
    print("=" * 60)
    print("1. Базовый пульт + Телевизор:")
    print("=" * 60)
    
    tv = TV()
    basic_remote_tv = BasicRemote(tv)
    
    basic_remote_tv.toggle_power()  
    basic_remote_tv.volume_up()
    basic_remote_tv.volume_up()
    basic_remote_tv.channel_up()
    basic_remote_tv.channel_up()
    basic_remote_tv.special_feature()
    basic_remote_tv.print_status()
    
    print("\n" + "=" * 60)
    print("2. Продвинутый пульт + Радио:")
    print("=" * 60)
    
    radio = Radio()
    advanced_remote_radio = AdvancedRemote(radio)
    
    advanced_remote_radio.toggle_power()  
    advanced_remote_radio.set_favorite_channel(101.2)
    advanced_remote_radio.special_feature()  
    advanced_remote_radio.special_feature()  
    advanced_remote_radio.volume_down()
    advanced_remote_radio.print_status()
    
    print("\n" + "=" * 60)
    print("3. Голосовой пульт + Телевизор:")
    print("=" * 60)
    
    tv2 = TV()
    voice_remote = VoiceRemote(tv2)
    
    voice_remote.toggle_power()  
    voice_remote.voice_command("Включи телевизор")
    voice_remote.voice_command("Сделай громче")
    voice_remote.voice_command("Переключи на канал 5")
    voice_remote.voice_command("Сделай тише")
    voice_remote.special_feature()
    voice_remote.print_status()
    
    print("\n" + "=" * 60)
    print("4. Мост в действии - меняем реализации независимо:")
    print("=" * 60)
    
    
    devices = [TV(), Radio(), SmartTV()]
    remote = AdvancedRemote(devices[0])  
    
    for i, device in enumerate(devices):
        print(f"\nУстройство {i+1}: {device.__class__.__name__}")
        
       
        remote._device = device
        
        remote.toggle_power()
        remote.volume_up()
        remote.channel_up()
        remote.special_feature()
        remote.print_status()
        remote.toggle_power()  
    
    print("\n" + "=" * 60)
    print("5. Умный пульт для SmartTV:")
    print("=" * 60)
    
    smart_tv = SmartTV()
    smart_remote = SmartRemote(smart_tv)
    
    smart_remote.toggle_power()
    smart_remote.launch_app("Netflix")
    smart_remote.set_brightness(75)
    smart_remote.volume_up()
    smart_remote.special_feature()
    smart_remote.print_status()
    
    print("\n" + "=" * 60)
    print("6. Преимущества Моста:")
    print("=" * 60)
    
    print("\nМожно комбинировать независимо:")
    print("- 3 типа устройств × 4 типа пультов = 12 комбинаций")
    
    combinations = [
        (BasicRemote, TV, "Базовый пульт + Телевизор"),
        (AdvancedRemote, Radio, "Продвинутый пульт + Радио"),
        (VoiceRemote, SmartTV, "Голосовой пульт + Умный ТВ"),
        (SmartRemote, TV, "Умный пульт + Обычный ТВ"),
    ]
    
    print("\nПримеры комбинаций:")
    for remote_class, device_class, description in combinations:
        device = device_class()
        remote = remote_class(device)
        print(f"  • {description}")
    
    print("\n✅ Мост работает корректно!")