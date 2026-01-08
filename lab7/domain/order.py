from dataclasses import dataclass, field
from typing import List
from decimal import Decimal
from datetime import datetime
from .money import Money


class OrderStatus:
    CREATED = "created"
    PAID = "paid"
    CANCELLED = "cancelled"


@dataclass
class OrderLine:
    """Строка заказа - часть агрегата Order"""
    product_id: str
    product_name: str
    price: Money
    quantity: int
    
    @property
    def total(self) -> Money:
        return self.price * self.quantity


@dataclass
class Order:
    """Агрегат Заказ - корневая сущность"""
    id: str
    customer_id: str
    lines: List[OrderLine] = field(default_factory=list)
    status: str = OrderStatus.CREATED
    created_at: datetime = field(default_factory=datetime.now)
    paid_at: datetime = None
    
    def add_line(self, product_id: str, product_name: str, price: Money, quantity: int):
        """Добавить товар в заказ"""
        if self.status == OrderStatus.PAID:
            raise ValueError("Cannot modify paid order")
        self.lines.append(OrderLine(product_id, product_name, price, quantity))
    
    def calculate_total(self) -> Money:
        """Рассчитать общую сумму заказа"""
        if not self.lines:
            return Money(Decimal("0"), "RUB")
        
        total = Money(Decimal("0"), self.lines[0].price.currency)
        for line in self.lines:
            total = total + line.total
        return total
    
    def pay(self):
        """Оплатить заказ (доменная операция)"""
        if not self.lines:
            raise ValueError("Cannot pay empty order")
        
        if self.status == OrderStatus.PAID:
            raise ValueError("Order already paid")
        
        self.status = OrderStatus.PAID
        self.paid_at = datetime.now()