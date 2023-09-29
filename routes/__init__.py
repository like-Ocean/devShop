from .user import user
from .product import product
from .order import order


routes = [
    user.user_router,
    product.product_router,
    order.order_router
]
