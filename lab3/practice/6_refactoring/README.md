# Лаба 6 - Рефакторинг и code smells

На лекции мы разобрали, что такое поддерживаемый код, code smells и рефакторинг.
В этой лабораторной работе нужно поработать с существующим кодом и улучшить его структуру без изменения поведения.

Цель работы - научиться:

* находить smells в реальном коде,
* делать рефакторинг маленькими шагами,
* применять DRY / KISS на практике,
* сохранять поведение при изменении структуры.

## Что нужно сделать

1. Создать или склонировать репозиторий для лабораторной работы
2. Запустить тесты и убедиться, что они проходят
3. Отрефакторить код в `order_processing.py`, не меняя поведение
4. Убедиться, что все тесты по-прежнему проходят
5. Добавить краткое описание проделанных изменений в `README.md`

Сдать ссылку на репозиторий.

## Содержание

### 1. Подготовка

Создать файл `order_processing.py` со следующим кодом:

```python
def parse_request(request: dict):
    user_id = request.get("user_id")
    items = request.get("items")
    coupon = request.get("coupon")
    currency = request.get("currency")
    return user_id, items, coupon, currency


def process_checkout(request: dict) -> dict:
    user_id, items, coupon, currency = parse_request(request)

    if user_id is None:
        raise ValueError("user_id is required")
    if items is None:
        raise ValueError("items is required")
    if currency is None:
        currency = "USD"

    if type(items) is not list:
        raise ValueError("items must be a list")
    if len(items) == 0:
        raise ValueError("items must not be empty")

    for it in items:
        if "price" not in it or "qty" not in it:
            raise ValueError("item must have price and qty")
        if it["price"] <= 0:
            raise ValueError("price must be positive")
        if it["qty"] <= 0:
            raise ValueError("qty must be positive")

    subtotal = 0
    for it in items:
        subtotal = subtotal + it["price"] * it["qty"]

    discount = 0
    if coupon is None or coupon == "":
        discount = 0
    elif coupon == "SAVE10":
        discount = int(subtotal * 0.10)
    elif coupon == "SAVE20":
        if subtotal >= 200:
            discount = int(subtotal * 0.20)
        else:
            discount = int(subtotal * 0.05)
    elif coupon == "VIP":
        discount = 50
        if subtotal < 100:
            discount = 10
    else:
        raise ValueError("unknown coupon")

    total_after_discount = subtotal - discount
    if total_after_discount < 0:
        total_after_discount = 0

    tax = int(total_after_discount * 0.21)
    total = total_after_discount + tax

    order_id = str(user_id) + "-" + str(len(items)) + "-" + "X"

    return {
        "order_id": order_id,
        "user_id": user_id,
        "currency": currency,
        "subtotal": subtotal,
        "discount": discount,
        "tax": tax,
        "total": total,
        "items_count": len(items),
    }
```

### 2. Тесты

Создать файл `test_order_processing.py`:

```python
import pytest
from order_processing import process_checkout


def test_ok_no_coupon():
    r = process_checkout({"user_id": 1, "items": [{"price": 50, "qty": 2}], "coupon": None, "currency": "USD"})
    assert r["subtotal"] == 100
    assert r["discount"] == 0
    assert r["tax"] == 21
    assert r["total"] == 121


def test_ok_save10():
    r = process_checkout({"user_id": 2, "items": [{"price": 30, "qty": 3}], "coupon": "SAVE10", "currency": "USD"})
    assert r["discount"] == 9


def test_ok_save20():
    r = process_checkout({"user_id": 3, "items": [{"price": 100, "qty": 2}], "coupon": "SAVE20", "currency": "USD"})
    assert r["discount"] == 40


def test_unknown_coupon():
    with pytest.raises(ValueError):
        process_checkout({"user_id": 1, "items": [{"price": 10, "qty": 1}], "coupon": "???", "currency": "USD"})
```

Убедиться, что тесты проходят до начала рефакторинга.

### 3. Рефакторинг

Отрефакторить код так, чтобы:

* функция `process_checkout` стала заметно короче
* логика была разбита на отдельные функции:

  * разбор запроса
  * валидация
  * подсчёт subtotal
  * расчёт скидки
  * расчёт налога
* магические числа были вынесены в константы
* код читался сверху вниз как сценарий
* все тесты продолжали проходить

### 4. README

В `README.md` описать:

* какие проблемы качества были найдены
* какие рефакторинги были применены
* что стало проще читать и менять
