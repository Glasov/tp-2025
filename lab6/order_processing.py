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
