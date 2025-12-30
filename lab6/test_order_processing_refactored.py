"""
Тесты для отрефакторенной версии
Должны проходить все тесты, как и для оригинальной версии
"""
import sys
sys.path.insert(0, '.')

from order_processing_refactored import process_checkout


def run_all_tests():
    """Запускает все тесты"""
    tests_passed = 0
    tests_failed = 0
    
    try:
        r = process_checkout({"user_id": 1, "items": [{"price": 50, "qty": 2}], "coupon": None, "currency": "USD"})
        assert r["subtotal"] == 100, f"Expected subtotal 100, got {r['subtotal']}"
        assert r["discount"] == 0, f"Expected discount 0, got {r['discount']}"
        assert r["tax"] == 21, f"Expected tax 21, got {r['tax']}"
        assert r["total"] == 121, f"Expected total 121, got {r['total']}"
        print("✅ Test 1 passed: No coupon")
        tests_passed += 1
    except AssertionError as e:
        print(f"❌ Test 1 failed: {e}")
        tests_failed += 1
    
    try:
        r = process_checkout({"user_id": 2, "items": [{"price": 30, "qty": 3}], "coupon": "SAVE10", "currency": "USD"})
        assert r["discount"] == 9, f"Expected discount 9, got {r['discount']}"
        print("✅ Test 2 passed: SAVE10 coupon")
        tests_passed += 1
    except AssertionError as e:
        print(f"❌ Test 2 failed: {e}")
        tests_failed += 1
    
    
    try:
        r = process_checkout({"user_id": 3, "items": [{"price": 100, "qty": 2}], "coupon": "SAVE20", "currency": "USD"})
        assert r["discount"] == 40, f"Expected discount 40, got {r['discount']}"
        print("✅ Test 3 passed: SAVE20 coupon")
        tests_passed += 1
    except AssertionError as e:
        print(f"❌ Test 3 failed: {e}")
        tests_failed += 1
    
   
    try:
        process_checkout({"user_id": 1, "items": [{"price": 10, "qty": 1}], "coupon": "???", "currency": "USD"})
        print("❌ Test 4 failed: Should raise ValueError for unknown coupon")
        tests_failed += 1
    except ValueError:
        print("✅ Test 4 passed: Unknown coupon raises ValueError")
        tests_passed += 1
    
    try:
        r = process_checkout({"user_id": 4, "items": [{"price": 20, "qty": 1}], "coupon": "", "currency": "EUR"})
        assert r["discount"] == 0, f"Expected discount 0 for empty coupon, got {r['discount']}"
        print("✅ Test 5 passed: Empty coupon")
        tests_passed += 1
    except AssertionError as e:
        print(f"❌ Test 5 failed: {e}")
        tests_failed += 1
    
   
    try:
        r = process_checkout({"user_id": 5, "items": [{"price": 90, "qty": 1}], "coupon": "VIP", "currency": "USD"})
        assert r["discount"] == 10, f"Expected discount 10 for VIP with subtotal < 100, got {r['discount']}"
        print("✅ Test 6 passed: VIP coupon with small subtotal")
        tests_passed += 1
    except AssertionError as e:
        print(f"❌ Test 6 failed: {e}")
        tests_failed += 1
    

    try:
        r = process_checkout({"user_id": 6, "items": [{"price": 150, "qty": 1}], "coupon": "VIP", "currency": "USD"})
        assert r["discount"] == 50, f"Expected discount 50 for VIP with subtotal >= 100, got {r['discount']}"
        print("✅ Test 7 passed: VIP coupon with large subtotal")
        tests_passed += 1
    except AssertionError as e:
        print(f"❌ Test 7 failed: {e}")
        tests_failed += 1
    
 
    print(f"\n{'='*50}")
    print(f"ИТОГ: {tests_passed} тестов прошло, {tests_failed} тестов упало")
    print(f"{'='*50}")
    
    if tests_failed == 0:
        print("��� Все тесты прошли успешно! Рефакторинг не сломал функциональность.")
    else:
        print("⚠️  Некоторые тесты не прошли. Проверь рефакторинг.")
    
    return tests_failed == 0


if __name__ == "__main__":
    run_all_tests()
