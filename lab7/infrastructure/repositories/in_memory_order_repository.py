from typing import Optional, Dict
from domain.order import Order
from interfaces.repositories import OrderRepository


class InMemoryOrderRepository(OrderRepository):
    """In-memory реализация репозитория заказов"""
    
    def __init__(self):
        self._orders: Dict[str, Order] = {}
    
    def get_by_id(self, order_id: str) -> Optional[Order]:
        return self._orders.get(order_id)
    
    def save(self, order: Order) -> None:
        self._orders[order.id] = order