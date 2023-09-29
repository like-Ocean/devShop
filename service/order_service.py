import datetime

from models import Order, OrderItem, Product, User


def make_order(user_id: int, address: str, products_id: list):
    customer = User.get_or_none(id=user_id)
    if not customer:
        return 'User not found'

    order = Order.create(
        user=customer,
        order_date=datetime.date.today(),
        address=address,
        status='Order in process'
    )

    for product_id in products_id:
        product = Product.get_or_none(Product.id == product_id['product_id'])
        OrderItem.create(
            order=order,
            product=product,
            count=product_id['count']
        )

    return order.get_dto()


def get_orders_info():
    pass


def get_order_info(order_id: int):
    pass


def delete_order(order_id: int):
    pass

