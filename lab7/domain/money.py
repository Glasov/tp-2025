from decimal import Decimal
from dataclasses import dataclass

@dataclass(frozen=True) 
class Money:
    amount: Decimal
    currency: str = "RUB"
    
    def __add__(self, other: 'Money') -> 'Money':
        if self.currency != other.currency:
            raise ValueError("Cannot add money with different currencies")
        return Money(self.amount + other.amount, self.currency)
    
    def __mul__(self, multiplier: int) -> 'Money':
        return Money(self.amount * Decimal(multiplier), self.currency)
    
    def __str__(self) -> str:
        return f"{self.amount} {self.currency}"