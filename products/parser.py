import re
from typing import Union

import requests
from bs4 import BeautifulSoup


class Parser:
    """Parser interface"""

    def download_page_text(self, url: str) -> str:
        raise NotImplementedError

    def get_parsed_items(self, *args, **kwargs):
        raise NotImplementedError


class CitilinkParser(Parser):
    """Parse a category products from citilink.ru"""

    def __init__(self, category_url: str):
        self.soup = self._get_soup(self.download_page_text(category_url))

    @staticmethod
    def _get_soup(html_text: str) -> BeautifulSoup:
        return BeautifulSoup(html_text, 'html.parser')

    def download_page_text(self, url: str) -> str:
        return requests.get(url).text

    def _download_detail_product_page_text(self, product_div):
        detail_url = product_div.find('a', class_='ProductCardHorizontal__title')['href']
        return self.download_page_text(f'https://www.citilink.ru{detail_url}')

    def _get_product_categories(self, product_div) -> list:
        """Return all product categories (sequence): from parent to child as list of names"""
        categories = []
        detail_page_soup = self._get_soup(self._download_detail_product_page_text(product_div))
        for category in detail_page_soup.findAll('div', class_='Breadcrumbs'):
            categories.append(category.find('span', itemprop='name').text)
        return categories

    @staticmethod
    def _get_product_price(product_div) -> Union[float, None]:
        price_div = product_div.find('span', class_='ProductCardHorizontal__price_current-price')
        try:
            return float(price_div.text)
        except AttributeError:
            return None
        except ValueError:
            try:
                return float(re.findall("\d+\.\d+", price_div.text)[0])
            except:
                return float(''.join(price_div.text.split(' ')))

    def get_parsed_items(self):
        """Return list of products: name, price, img_url, categories"""
        products = []

        for product in self.soup.findAll('div', class_='ProductCardHorizontal'):
            price = self._get_product_price(product)
            if price is None:
                continue

            name = product.find('a', class_='ProductCardHorizontal__title')['title']
            img_url = product.find('div', class_='ProductCardHorizontal__picture-hover_part')['data-src']
            products.append({
                'name': name,
                'price': price,
                'img_url': img_url,
                'categories': self._get_product_categories(product)
            })

        return products
