import datetime
from models import Order, OrderItem, Product, User

ORDER_STATUS = ['IN_PROCESSING', 'ACCEPTED_FOR_EXECUTION', 'SENT', 'ORDER_RECEIVED']


# возможно нужно будет чуть переписать, чтобы товары добавлялись тут, а адресс и дата в другой функции
def check_products_availability(products_id: list):
    for product_id in products_id:
        product = Product.get_or_none(Product.id == product_id['product_id'])
        if not product:
            return f'Product {product_id["product_id"]} not found'

        if product.total_count < product_id['count']:
            return f"There are only {product.total_count} units of the {product.name} in stock."


def product_reduction(product_id: int, count: int):
    product = Product.get_or_none(Product.id == product_id)
    if product:
        product.total_count -= count
        product.save()


def make_order(user_id: int, address: str, products_id: list):
    customer = User.get_or_none(id=user_id)
    if not customer:
        return 'User not found'

    available_product = check_products_availability(products_id)
    if available_product is not None:
        return available_product

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
        product_reduction(product_id['product_id'], product_id['count'])

    return order.get_dto()


# написать роут и протестировать
def change_order(order_id: int, new_address: str, products_id: list):
    order = Order.get_or_none(Order.id == order_id)
    if not order:
        return 'Order not found'

    if order.status != 'IN_PROCESSING':
        return 'Order cannot be changed'

    available_product = check_products_availability(products_id)
    if available_product is not None:
        return available_product

    order.address = new_address
    order.save()

    for product_id in products_id:
        order_item = OrderItem.get_or_none(
            (OrderItem.order == order_id) & (OrderItem.product == product_id['product_id'])
        )
        if not order_item:
            return f'Product {product_id["product_id"]} not found in the order'

        product_reduction(product_id['product_id'], product_id['count'])

    return order.get_dto()


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
