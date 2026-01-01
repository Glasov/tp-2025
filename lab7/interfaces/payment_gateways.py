from abc import ABC, abstractmethod
from domain.money import Money


class PaymentGateway(ABC):
    """Интерфейс платежного шлюза"""
    
    @abstractmethod
    def charge(self, order_id: str, amount: Money) -> str:
        """
        Выполнить платеж
        
        Args:
            order_id: ID заказа
            amount: Сумма к оплате
            
        Returns:
            ID транзакции
        """
        pass