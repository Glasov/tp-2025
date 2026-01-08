import unittest
from decimal import Decimal
from domain.money import Money
from domain.order import Order, OrderStatus
from infrastructure.repositories.in_memory_order_repository import InMemoryOrderRepository
from infrastructure.payment_gateways.fake_payment_gateway import FakePaymentGateway
from application.use_cases.pay_order_use_case import PayOrderUseCase


class TestPayOrderUseCase(unittest.TestCase):
    
    def setUp(self):
        """Настройка перед каждым тестом"""
        self.order_repo = InMemoryOrderRepository()
        self.payment_gateway = FakePaymentGateway()
        self.use_case = PayOrderUseCase(self.order_repo, self.payment_gateway)
    
    def test_successful_payment(self):
        """Успешная оплата корректного заказа"""
      
        order = Order(id="order-1", customer_id="customer-1")
        order.add_line("prod-1", "Product 1", Money(Decimal("100.50"), "RUB"), 2)
        order.add_line("prod-2", "Product 2", Money(Decimal("50.25"), "RUB"), 1)
        
        
        self.order_repo.save(order)
        
        
        transaction_id = self.use_case.execute("order-1")
        
       
        self.assertIsNotNone(transaction_id)
        
       
        paid_order = self.order_repo.get_by_id("order-1")
        self.assertEqual(paid_order.status, OrderStatus.PAID)
        self.assertIsNotNone(paid_order.paid_at)
        
   
        self.assertEqual(str(paid_order.calculate_total()), "251.25 RUB")
    
    def test_payment_empty_order(self):
        """Ошибка при оплате пустого заказа"""
        order = Order(id="order-2", customer_id="customer-1")
        self.order_repo.save(order)
        
        with self.assertRaises(ValueError) as context:
            self.use_case.execute("order-2")
        
        self.assertIn("Cannot pay empty order", str(context.exception))
    
    def test_double_payment(self):
        """Ошибка при повторной оплате"""
        order = Order(id="order-3", customer_id="customer-1")
        order.add_line("prod-1", "Product 1", Money(Decimal("100"), "RUB"), 1)
        self.order_repo.save(order)
        
        self.use_case.execute("order-3")
        
        
        with self.assertRaises(ValueError) as context:
            self.use_case.execute("order-3")
        
        self.assertIn("Order already paid", str(context.exception))
    
    def test_cannot_modify_after_payment(self):
        """Невозможность изменения заказа после оплаты"""
        order = Order(id="order-4", customer_id="customer-1")
        order.add_line("prod-1", "Product 1", Money(Decimal("100"), "RUB"), 1)
        self.order_repo.save(order)
        
       
        self.use_case.execute("order-4")
        
      
        paid_order = self.order_repo.get_by_id("order-4")
        with self.assertRaises(ValueError) as context:
            paid_order.add_line("prod-2", "Product 2", Money(Decimal("50"), "RUB"), 1)
        
        self.assertIn("Cannot modify paid order", str(context.exception))


if __name__ == '__main__':
    unittest.main()