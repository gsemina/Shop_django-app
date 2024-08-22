from django.core.management import BaseCommand

from shopapp.models import Product


class Command(BaseCommand):
    """Creates new products"""
    def handle(self, *args, **options):
        self.stdout.write("Create Products")

        products_names = [
            "Laptop",
            "Desctop",
            "Smartpnone",
        ]
        for product_name in products_names:
            product, created = Product.objects.get_or_create(name=product_name)
            self.stdout.write(f"Created Product {product_name} ")

        self.stdout.write(self.style.SUCCESS('Product created'))
