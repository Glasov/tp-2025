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
