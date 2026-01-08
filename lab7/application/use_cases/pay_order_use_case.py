from interfaces.repositories import OrderRepository
from interfaces.payment_gateways import PaymentGateway


class PayOrderUseCase:
    """Use Case: Оплата заказа"""
    
    def __init__(self, order_repo: OrderRepository, payment_gateway: PaymentGateway):
        self.order_repo = order_repo
        self.payment_gateway = payment_gateway
    
    def execute(self, order_id: str) -> str:
        """
        Выполнить оплату заказа
        
        Steps:
        1. Загрузить заказ через OrderRepository
        2. Выполнить доменную операцию оплаты
        3. Вызвать платёж через PaymentGateway
        4. Сохранить заказ
        5. Вернуть результат оплаты
        """
      
        order = self.order_repo.get_by_id(order_id)
        if not order:
            raise ValueError(f"Order {order_id} not found")
        
        
        total_amount = order.calculate_total()
        
        transaction_id = self.payment_gateway.charge(order_id, total_amount)
        
       
        order.pay()
        
       
        self.order_repo.save(order)
        
        return transaction_id