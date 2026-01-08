# Лабораторная работа 7: Clean Architecture и DDD-lite

## Описание
Реализация системы оплаты заказов с использованием Clean Architecture и принципов DDD-lite.

## Структура проекта

### Domain Layer (Доменный слой)
- `domain/money.py` - Value Object Money
- `domain/order.py` - Агрегат Order, сущность OrderLine, OrderStatus

### Application Layer (Слой приложения)
- `application/use_cases/pay_order_use_case.py` - Use Case оплаты заказа

### Infrastructure Layer (Инфраструктурный слой)
- `infrastructure/repositories/in_memory_order_repository.py` - Репозиторий заказов в памяти
- `infrastructure/payment_gateways/fake_payment_gateway.py` - Фейковый платежный шлюз

### Interfaces Layer (Слой интерфейсов)
- `interfaces/repositories.py` - Интерфейс OrderRepository
- `interfaces/payment_gateways.py` - Интерфейс PaymentGateway

### Tests
- `tests/test_pay_order_use_case.py` - Тесты Use Case

## Требования и инварианты доменной модели

1. **Order** - сущность (агрегат)
2. **OrderLine** - часть агрегата Order
3. **Money** - value object
4. **OrderStatus** - перечисление статусов

### Инварианты:
- ❌ Нельзя оплатить пустой заказ
- ❌ Нельзя оплатить заказ повторно
- ❌ После оплаты нельзя менять строки заказа
- ✅ Итоговая сумма равна сумме строк

## Запуск

### Демонстрация работы:
```bash
python main.py