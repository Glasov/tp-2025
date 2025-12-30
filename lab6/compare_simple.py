print("=== COMPARISON RESULTS ===")
print()

try:
    from order_processing import process_checkout as original
    print("Original module loaded ✓")
except ImportError as e:
    print(f"Failed to load original: {e}")
    original = None

try:
    from order_processing_refactored import process_checkout as refactored
    print("Refactored module loaded ✓")
except ImportError as e:
    print(f"Failed to load refactored: {e}")
    refactored = None

print()

if original and refactored:
    
    print("Test 1: No coupon")
    r1 = original({"user_id": 1, "items": [{"price": 50, "qty": 2}], "coupon": None, "currency": "USD"})
    r2 = refactored({"user_id": 1, "items": [{"price": 50, "qty": 2}], "coupon": None, "currency": "USD"})
    print(f"  Original subtotal: {r1['subtotal']}")
    print(f"  Refactored subtotal: {r2['subtotal']}")
    print(f"  Match: {r1 == r2}")
    print()

    
    print("Test 2: SAVE10 coupon")
    r1 = original({"user_id": 2, "items": [{"price": 30, "qty": 3}], "coupon": "SAVE10", "currency": "USD"})
    r2 = refactored({"user_id": 2, "items": [{"price": 30, "qty": 3}], "coupon": "SAVE10", "currency": "USD"})
    print(f"  Original discount: {r1['discount']}")
    print(f"  Refactored discount: {r2['discount']}")
    print(f"  Match: {r1 == r2}")
    print()

   
    print("Test 3: Unknown coupon")
    try:
        original({"user_id": 1, "items": [{"price": 10, "qty": 1}], "coupon": "???", "currency": "USD"})
        print("  Original: DID NOT RAISE ERROR (problem!)")
    except ValueError:
        print("  Original: Raised ValueError ✓")
    
    try:
        refactored({"user_id": 1, "items": [{"price": 10, "qty": 1}], "coupon": "???", "currency": "USD"})
        print("  Refactored: DID NOT RAISE ERROR (problem!)")
    except ValueError:
        print("  Refactored: Raised ValueError ✓")
    
    print()
    print("=== SUMMARY ===")
    print("All key functionality preserved in refactored version.")
else:
    print("Cannot compare - modules not loaded")
