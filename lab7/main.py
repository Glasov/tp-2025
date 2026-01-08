from decimal import Decimal
from domain.money import Money
from domain.order import Order
from infrastructure.repositories.in_memory_order_repository import InMemoryOrderRepository
from infrastructure.payment_gateways.fake_payment_gateway import FakePaymentGateway
from application.use_cases.pay_order_use_case import PayOrderUseCase


def main():
    print("=== Лабораторная работа 7: Clean Architecture - Система оплаты заказов ===")
    print()
    
    
    order_repo = InMemoryOrderRepository()
    payment_gateway = FakePaymentGateway()
    pay_order_use_case = PayOrderUseCase(order_repo, payment_gateway)
    
    order = Order(id="order-001", customer_id="customer-123")
    order.add_line("prod-1", "Ноутбук", Money(Decimal("75000.00"), "RUB"), 1)
    order.add_line("prod-2", "Мышь", Money(Decimal("2500.50"), "RUB"), 2)
    order.add_line("prod-3", "Сумка", Money(Decimal("3000.00"), "RUB"), 1)
  
    order_repo.save(order)
    
    print("📦 Создан заказ:")
    print(f"   ID: {order.id}")
    print(f"   Клиент: {order.customer_id}")
    print(f"   Товаров: {len(order.lines)}")
    print(f"   Итоговая сумма: {order.calculate_total()}")
    print()
    
   
    print("💳 Пробуем оплатить заказ...")
    try:
        transaction_id = pay_order_use_case.execute("order-001")
        print(f"✅ Успех! ID транзакции: {transaction_id}")
        print()
        
       
        paid_order = order_repo.get_by_id("order-001")
        print("📋 Статус заказа после оплаты:")
        print(f"   Статус: {paid_order.status}")
        print(f"   Дата оплаты: {paid_order.paid_at}")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    
    print()
    print("=" * 60)
    print("Структура проекта по Clean Architecture:")
    print("1. Domain Layer: Order, OrderLine, Money, OrderStatus")
    print("2. Application Layer: PayOrderUseCase")
    print("3. Infrastructure Layer: InMemoryOrderRepository, FakePaymentGateway")
    print("4. Interfaces Layer: OrderRepository, PaymentGateway")
    print("5. Tests: test_pay_order_use_case.py")


if __name__ == "__main__":
    main()