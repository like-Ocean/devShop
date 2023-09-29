from werkzeug.utils import secure_filename
import os
from models import Product, ProductImg, Category


def add_category(name: str, slug: str):
    category = Category.get_or_none(name=name)
    if category:
        return 'category already exists'

    category = Category(
        name=name,
        slug=slug
    )
    category.save()
    return category.get_dto()


def remove_category(category_id: int):
    category = Category.get_or_none(Category.id == category_id)
    if not category:
        return 'Category not found', 401
    Category.delete().where(Category.id == category_id).execute()
    return 200


def get_categories():
    categories = Category.select()
    return [category.get_dto() for category in categories]


def get_category(category_id: int):
    category = Category.get_or_none(id=category_id)
    if not category:
        return 'Category not found'
    return category.get_dto()


def add_product(
        category_id: int, name: str, description: str,
        price: float, discount: int, total_count: int
):
    if discount != 0:
        discount_price = price / 100 * discount
        final_price = price - discount_price
    else:
        final_price = price
    product = Product(
        category=category_id,
        name=name,
        description=description,
        price=price,
        discount=discount,
        final_price=final_price,
        total_count=total_count
    )
    product.save()
    return product.get_dto()


def change_product(
        product_id: int, category_id: int, name: str, description: str,
        price: float, discount: int, total_count: int
):
    product = Product.get_or_none(Product.id == product_id)
    if not product:
        return 'Product not found'

    if discount != 0:
        discount_price = price / 100 * discount
        final_price = price - discount_price
    else:
        final_price = price

    product.category = category_id
    product.name = name
    product.description = description
    product.price = price
    product.discount = discount
    product.final_price = final_price
    product.total_count = total_count
    product.save()

    return product.get_dto()


def get_products():
    products = Product.select()
    imgs = ProductImg.select()

    img_dict = {img.product.id: img.url for img in imgs}

    product_list = []
    for product in products:
        product_dto = product.get_dto()
        product_dto['img_url'] = img_dict.get(product.id)
        product_list.append(product_dto)

    return product_list


def get_product(product_id: int):
    product = Product.get_or_none(id=product_id)
    if not product:
        return 'Product not found'

    return product.get_dto()


def remove_product(product_id: int):
    product = Product.get_or_none(id=product_id)
    if not product:
        return 'Product not found'

    product_imgs = ProductImg.select().where(ProductImg.product == product_id)
    for img in product_imgs:
        os.remove(img.url)

    Product.delete().where(Product.id == product_id).execute()
    ProductImg.delete().where(ProductImg.product == product_id).execute()

    return 200


def get_in_category_products(category_id: int):
    category = Category.get_or_none(id=category_id)
    if not category:
        return 'Category not found'

    products = Product.select().where(Product.category == category_id)

    return [product.get_dto() for product in products]


def ensure_folder_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


def save_file_to_folder(file, folder_path, filename):
    file_path = os.path.join(folder_path, filename)
    file.save(file_path)
    return file_path


def add_product_img(product_id, file):
    product = Product.get_or_none(Product.id == product_id)
    if not product:
        return 'Product not found'

    if not file:
        return 'You have not selected a file'

    filename = secure_filename(file.filename)
    folder_path = os.environ.get("FILES_FOLDER")
    ensure_folder_exists(folder_path)
    file_path = save_file_to_folder(file, folder_path, filename)

    new_file = ProductImg(
        product=product_id,
        url=file_path,
        filename=filename
    )
    new_file.save()

    return new_file.get_dto()


def remove_product_img(img_id: int):
    img = ProductImg.get_or_none(id=img_id)
    if not img:
        return 'Image not found'
    os.remove(img.url)
    ProductImg.delete().where(ProductImg.id == img_id).execute()
    return 200
