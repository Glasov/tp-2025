from abc import ABC, abstractmethod


class Transport(ABC):
    """Абстрактный класс транспорта"""
    @abstractmethod
    def deliver(self) -> str:
        pass


class Truck(Transport):
    """Грузовик - доставка по суше"""
    def deliver(self) -> str:
        return "🚚 Грузовик доставляет товары по дороге"


class Ship(Transport):
    """Корабль - доставка по морю"""
    def deliver(self) -> str:
        return "🚢 Корабль доставляет товары по морю"


class Plane(Transport):
    """Самолёт - доставка по воздуху"""
    def deliver(self) -> str:
        return "✈️ Самолёт доставляет товары по воздуху"



class Logistics(ABC):
    """
    Абстрактный класс логистики.
    Определяет фабричный метод create_transport()
    """
    @abstractmethod
    def create_transport(self) -> Transport:
        pass

    def plan_delivery(self) -> str:
        """
        Общий метод для планирования доставки.
        Не зависит от конкретного типа транспорта.
        """
        transport = self.create_transport()
        result = transport.deliver()
        return f"Планирование доставки: {result}"


class RoadLogistics(Logistics):
    """Дорожная логистика создаёт грузовики"""
    def create_transport(self) -> Transport:
        return Truck()


class SeaLogistics(Logistics):
    """Морская логистика создаёт корабли"""
    def create_transport(self) -> Transport:
        return Ship()


class AirLogistics(Logistics):
    """Воздушная логистика создаёт самолёты"""
    def create_transport(self) -> Transport:
        return Plane()


if __name__ == "__main__":
    print("=== Тест паттерна Factory Method ===\n")

    
    road_logistics = RoadLogistics()
    sea_logistics = SeaLogistics()
    air_logistics = AirLogistics()

    
    deliveries = [
        road_logistics.plan_delivery(),
        sea_logistics.plan_delivery(),
        air_logistics.plan_delivery()
    ]

    for delivery in deliveries:
        print(f"✓ {delivery}")

   
    print("\n=== Гибкость фабричного метода ===")
    
  
    class TrainLogistics(Logistics):
        def create_transport(self):
            class Train(Transport):
                def deliver(self):
                    return "🚂 Поезд доставляет товары по рельсам"
            return Train()

    train_logistics = TrainLogistics()
    print(f"✓ {train_logistics.plan_delivery()}")

    print("\n✅ Factory Method работает корректно!")