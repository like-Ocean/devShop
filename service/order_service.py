import datetime
from models import Order, OrderItem, Product, User

ORDER_STATUS = ['IN_PROCESSING', 'ACCEPTED_FOR_EXECUTION', 'SENT', 'ORDER_RECEIVED']


# возможно нужно будет чуть переписать, чтобы товары добавлялись тут, а адресс и дата в другой функции
# сделать вычет из product.total_count - product_id['count'].(уменьшение товара крч)
def make_order(user_id: int, address: str, products_id: list):
    customer = User.get_or_none(id=user_id)
    if not customer:
        return 'User not found'

    order = Order.create(
        user=customer,
        order_date=datetime.date.today(),
        address=address,
        status='IN_PROCESSING'
    )

    for product_id in products_id:
        product = Product.get_or_none(Product.id == product_id['product_id'])
        OrderItem.create(
            order=order,
            product=product,
            count=product_id['count']
        )

    return order.get_dto()


def change_order(order_id: int):
    pass


def get_orders_info():
    orders = Order.select()
    return [order.get_dto() for order in orders]


def get_order_info(order_id: int):
    order = Order.get_or_none(id=order_id)
    if not order:
        return 'Order not found'

    products = OrderItem.select().where(OrderItem.order == order_id)
    if not products:
        return 'Products not found'

    return [product.get_dto() for product in products]


def delete_order(order_id: int):
    order = Order.get_or_none(id=order_id)
    if not order:
        return 'Order not found'

    if order.status == 'ORDER_RECEIVED' or 'IN_PROCESSING':
        Order.delete().where(Order.id == order_id).execute()
        return 204
