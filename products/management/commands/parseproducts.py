from django.core.management.base import BaseCommand

from products.parser import CitilinkParser
from products.services import create_parsed_products


class Command(BaseCommand):
    help = 'Parse products and save them to DB'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Processing... 🚀'))
        create_parsed_products(parser=CitilinkParser('https://www.citilink.ru/catalog/smartfony/'))
        self.stdout.write(self.style.SUCCESS('Successfully parsed products 🎉'))
