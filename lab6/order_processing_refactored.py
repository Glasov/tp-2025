"""
Рефакторинг кода обработки заказов
Улучшения:
1. Вынесены магические числа в константы
2. Разделена логика на маленькие функции
3. Улучшена читаемость
4. Сохранено исходное поведение
"""


DEFAULT_CURRENCY = "USD"
DEFAULT_TAX_RATE = 0.21
MIN_PRICE = 0
MIN_QTY = 0

COUPON_DISCOUNTS = {
    "SAVE10": 0.10,
    "SAVE20": {"threshold": 200, "high": 0.20, "low": 0.05},
    "VIP": {"base": 50, "min_subtotal": 100, "fallback": 10}
}


def parse_request(request: dict) -> tuple:
    """Извлекает данные из запроса"""
    return (
        request.get("user_id"),
        request.get("items"),
        request.get("coupon"),
        request.get("currency")
    )


def validate_user_id(user_id):
    """Проверяет наличие user_id"""
    if user_id is None:
        raise ValueError("user_id is required")


def validate_items(items):
    """Валидирует список товаров"""
    if items is None:
        raise ValueError("items is required")
    
    if not isinstance(items, list):
        raise ValueError("items must be a list")
    
    if len(items) == 0:
        raise ValueError("items must not be empty")
    
    for item in items:
        if "price" not in item or "qty" not in item:
            raise ValueError("item must have price and qty")
        if item["price"] <= MIN_PRICE:
            raise ValueError("price must be positive")
        if item["qty"] <= MIN_QTY:
            raise ValueError("qty must be positive")


def calculate_subtotal(items: list) -> int:
    """Вычисляет общую стоимость товаров"""
    subtotal = 0
    for item in items:
        subtotal += item["price"] * item["qty"]
    return subtotal


def calculate_discount(coupon: str, subtotal: int) -> int:
    """Вычисляет размер скидки по купону"""
    if coupon is None or coupon == "":
        return 0
    
    if coupon not in COUPON_DISCOUNTS:
        raise ValueError("unknown coupon")
    
    discount_info = COUPON_DISCOUNTS[coupon]
    
    if coupon == "SAVE10":
        return int(subtotal * discount_info)
    
    elif coupon == "SAVE20":
        if subtotal >= discount_info["threshold"]:
            return int(subtotal * discount_info["high"])
        else:
            return int(subtotal * discount_info["low"])
    
    elif coupon == "VIP":
        if subtotal >= discount_info["min_subtotal"]:
            return discount_info["base"]
        else:
            return discount_info["fallback"]
    
    return 0


def calculate_tax(amount: int, tax_rate: float = DEFAULT_TAX_RATE) -> int:
    """Вычисляет налог"""
    return int(amount * tax_rate)


def generate_order_id(user_id, items_count: int) -> str:
    """Генерирует ID заказа"""
    return f"{user_id}-{items_count}-X"


def process_checkout(request: dict) -> dict:
    """Основная функция обработки заказа (рефакторенная)"""
   
    user_id, items, coupon, currency = parse_request(request)
    
  
    validate_user_id(user_id)
    validate_items(items)
    
    if currency is None:
        currency = DEFAULT_CURRENCY
    
  
    subtotal = calculate_subtotal(items)
    discount = calculate_discount(coupon, subtotal)
    
    total_after_discount = subtotal - discount
    if total_after_discount < 0:
        total_after_discount = 0
    
    tax = calculate_tax(total_after_discount)
    total = total_after_discount + tax
    
   
    order_id = generate_order_id(user_id, len(items))
    
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
