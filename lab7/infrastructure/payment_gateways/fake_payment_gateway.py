import uuid
from domain.money import Money
from interfaces.payment_gateways import PaymentGateway


class FakePaymentGateway(PaymentGateway):
    """Фейковый платежный шлюз для тестирования"""
    
    def charge(self, order_id: str, amount: Money) -> str:
        transaction_id = str(uuid.uuid4())
        print(f"[FakePaymentGateway] Charging {amount} for order {order_id}")
        print(f"[FakePaymentGateway] Transaction ID: {transaction_id}")
        return transaction_id