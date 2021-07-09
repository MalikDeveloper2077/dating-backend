import os
from django.core.files import File

from products.models import Category, Product
from products.parser import Parser
from products.utils import get_downloaded_img


def create_or_get_category(name: str, parent_name: str = None):
    category, created = Category.objects.get_or_create(name=name)
    if parent_name:
        parent_category, created = Category.objects.get_or_create(name=parent_name)
        category.parent_category = parent_category
        category.save(update_fields=('parent_category',))
    return category


def create_product(name: str, price: float, img_url: str, category: Category):
    """Create product and save the image by getting it from img_url"""
    product = Product.objects.create(name=name, price=price, category=category)
    product.image.save(
        os.path.basename(img_url),
        File(get_downloaded_img(img_url)),
        save=True
    )
    product.save()


def create_parsed_products(parser: Parser):
    """Parse products from the parser and save them in DB"""
    for product in parser.get_parsed_items():
        categories = product['categories']
        product_main_category = None
        for idx, category_name in enumerate(categories):
            try:
                product_main_category = create_or_get_category(name=category_name, parent_name=categories[idx - 1])
            except IndexError:
                product_main_category = create_or_get_category(name=category_name)

        product.pop('categories')
        create_product(**product, category=product_main_category)
