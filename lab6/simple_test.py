from order_processing_refactored import process_checkout

print("Testing refactored code...")
print("=" * 50)

try:
    r = process_checkout({"user_id": 1, "items": [{"price": 50, "qty": 2}], "coupon": None, "currency": "USD"})
    assert r["subtotal"] == 100
    assert r["discount"] == 0
    assert r["tax"] == 21
    assert r["total"] == 121
    print("✅ Test 1: No coupon - PASSED")
except Exception as e:
    print(f"❌ Test 1: No coupon - FAILED: {e}")


try:
    r = process_checkout({"user_id": 2, "items": [{"price": 30, "qty": 3}], "coupon": "SAVE10", "currency": "USD"})
    assert r["discount"] == 9
    print("✅ Test 2: SAVE10 coupon - PASSED")
except Exception as e:
    print(f"❌ Test 2: SAVE10 coupon - FAILED: {e}")


try:
    r = process_checkout({"user_id": 3, "items": [{"price": 100, "qty": 2}], "coupon": "SAVE20", "currency": "USD"})
    assert r["discount"] == 40
    print("✅ Test 3: SAVE20 coupon - PASSED")
except Exception as e:
    print(f"❌ Test 3: SAVE20 coupon - FAILED: {e}")

try:
    process_checkout({"user_id": 1, "items": [{"price": 10, "qty": 1}], "coupon": "???", "currency": "USD"})
    print("❌ Test 4: Unknown coupon - FAILED (should raise error)")
except ValueError:
    print("✅ Test 4: Unknown coupon - PASSED (correctly raised error)")

print("=" * 50)
print("Testing completed!")
