from django.core.management import BaseCommand
from BlogApp.models import Category


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Create category")
        catigories_names = [
            ('Информационная статья'),
            ('Передовая статья'),
            ('Научная статья'),
        ]
        categories = [Category(name=name) for name in catigories_names]
        Category.objects.bulk_create(categories)

        self.stdout.write("Done")